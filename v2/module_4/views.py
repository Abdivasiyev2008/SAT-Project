from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Module_4, Module_4_Question, Practice, Time4
from certificate.models import Certificate, Checking
from module_4.calc import calculate_scaled_score
from django_user_agents.utils import get_user_agent
from module_2.calc import get_scaled_score
from django.db import transaction
from django.utils.timezone import now


@login_required
def module_4_Detail(request, pk):
    user_agent = get_user_agent(request)
    
    # Retrieve the Practice object or return a 404 if not found
    practice = get_object_or_404(Practice, id=pk)

    # Check if the user has already completed module 4
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module4')

    if certificate_data.exists() and certificate_data[0]['module4']:
        return redirect(f'/tests/{pk}/certificate/get')  # Redirect to the certificate page if already completed

    if user_agent.is_pc or user_agent.is_tablet:
        # Retrieve the questions related to the practice
        module_4_questions = Module_4_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        # If the user has already completed the checking process, redirect
        if check.exists():
            return redirect(f'/tests/{pk}/certificate/get')

        # If no questions are available, show a message
        if not module_4_questions.exists():
            return render(request, 'modules/module_4.html', {'message': 'No questions available for this test.'})
    
        # Timer uchun vaqtni olish yoki yangisini yaratish
        time_obj, created = Time4.objects.get_or_create(
            user=request.user,
            practice=practice,
            defaults={"time": 32 * 60}  # 32 daqiqa
        )

        # Saqlangan vaqtni yangilangan holda qaytarish
        last_updated = time_obj.updated_at if hasattr(time_obj, 'updated_at') else None
        if last_updated:
            elapsed_time = (now() - last_updated).total_seconds()
            remaining_time = max(0, time_obj.time - int(elapsed_time))
            time_obj.time = remaining_time
            time_obj.save()
        else:
            remaining_time = time_obj.time

        context = {
            'practice': practice,
            'questions': module_4_questions,
            'total_questions': module_4_questions.count(),
            'remaining_time': remaining_time,  # Timer uchun qoldiq vaqt
        }

        return render(request, 'modules/module_4.html', context)
    
    # If the user is on a mobile or other non-PC device
    return HttpResponse("If you want to use this platform, please use a computer.")  # For mobile and other devices

@csrf_exempt
def save_time(request, pk):
    """AJAX orqali vaqtni saqlash."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            remaining_time = data.get("time")

            if remaining_time is None:
                return JsonResponse({"error": "Time data is missing."}, status=400)

            practice = get_object_or_404(Practice, id=pk)

            # Vaqtni yangilash yoki yaratish
            time_obj, created = Time4.objects.get_or_create(
                user=request.user,
                practice=practice,
                defaults={"time": remaining_time}
            )
            if not created:
                time_obj.time = remaining_time
                time_obj.updated_at = now()  # `now()` funksiyasi bilan yangilash
                time_obj.save()

            return JsonResponse({"message": "Time saved successfully.", "remaining_time": time_obj.time})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def submit_quiz(request, pk):
    user_agent = get_user_agent(request)

    # Ensure the user is on a PC or tablet
    if user_agent.is_pc or user_agent.is_tablet:
        if request.method == "POST":
            try:
                # Parse incoming JSON data
                data = json.loads(request.body)
                print("Received JSON data:", data)  # Debug log
                answers = data.get("answers", {})  # Ensure we get an empty dict if no answers are provided

                # Retrieve the practice and related questions
                practice = get_object_or_404(Practice, id=pk)
                questions = Module_4_Question.objects.filter(module__practice=practice)

                if not questions.exists():
                    return JsonResponse({"error": "No questions found for this practice."}, status=404)

                # Get or create the certificate object
                certificate, created = Certificate.objects.get_or_create(
                    practice=practice,
                    user=request.user,
                    defaults={
                        'math': 0,
                        'overall': 0,
                        'english': 0,
                    }
                )

                # If module4 is already completed, skip the submission
                if certificate.module4:
                    return JsonResponse({
                        "message": "You have already completed this module.",
                        "score": certificate.math  # Return the existing score if already completed
                    })

                # Calculate score based on the answers provided
                score = 0
                if answers:  # If there are answers, check and calculate the score
                    for question, user_answer in zip(questions, answers.values()):
                        if user_answer == question.option_select_answer or user_answer == question.option_input_answer:
                            score += 1

                # Update certificate with new score
                score = calculate_scaled_score(int(score) + int(certificate.math))  # Calculate scaled score
                certificate.math = score
                certificate.english = get_scaled_score(certificate.english)  # Assuming you have a method for this
                certificate.module4 = True

                # Ensure there are no None values in the certificate fields
                certificate.overall = int(certificate.math) + int(certificate.english)
                certificate.save()

                return JsonResponse({"message": "Quiz submitted successfully", "score": score})

            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)  # Debug log
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            except Exception as e:
                print(f"Unexpected error: {e}")  # Debug log
                return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

        return JsonResponse({"error": "Invalid request method"}, status=405)  # Only POST is allowed

    return HttpResponse("If you want to use this platform, please use a computer.")  # For mobile and other devices
