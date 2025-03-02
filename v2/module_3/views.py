from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import json
from .models import Module_3, Module_3_Question, Practice, Time3
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent
from django.db import transaction
from correct.models import *
from django.db import IntegrityError


@login_required
def module_3_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Retrieve the Practice object or return a 404 if not found
    practice = get_object_or_404(Practice, id=pk)

    # Check if the user has completed this module
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module3')

    if certificate_data.exists():
        module3_value = certificate_data[0]['module3']
        if module3_value:  # If module3 is already completed, redirect to the next step
            return redirect(f'/tests/practice/{pk}/4/')

    # Handle requests only from PC or tablet
    if user_agent.is_pc or user_agent.is_tablet:
        # Retrieve the questions related to the practice
        module_3_questions = Module_3_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if check.exists():
            return redirect(f'/tests/{pk}/certificate/get')

        # If no questions are available, show a message
        if not module_3_questions.exists():
            return render(request, 'modules/module_3.html', {'message': 'No questions available for this test.'})

        # Timer functionality: Retrieve or create a Time3 object for the user
        time_obj, created = Time3.objects.get_or_create(
            user=request.user,
            practice=practice,
            defaults={"time": 30 * 60}  # Default time set to 30 minutes
        )

        # Update remaining time based on the last update
        last_updated = time_obj.updated_at if hasattr(time_obj, 'updated_at') else None
        if last_updated:
            elapsed_time = (now() - last_updated).total_seconds()
            remaining_time = max(0, time_obj.time - int(elapsed_time))
            time_obj.time = remaining_time
            time_obj.save()
        else:
            remaining_time = time_obj.time

        # Prepare context to pass to the template
        context = {
            'practice': practice,
            'questions': module_3_questions,
            'total_questions': module_3_questions.count(),
            'remaining_time': remaining_time,  # Timer for the module
        }

        return render(request, 'modules/module_3.html', context)

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")

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
            time_obj, created = Time3.objects.get_or_create(
                user=request.user,
                practice=practice,
                defaults={"time": remaining_time}
            )
            if not created:
                time_obj.time = remaining_time
                time_obj.updated_at = now()  # `now()` funksiyasi bilan yangilash
                time_obj.save()

            return JsonResponse({"message": "Time saved successfully.", "remaining_time": time_obj.time})
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)  # Debug log
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except Exception as e:
            print(f"Unexpected error: {e}")  # Debug log
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)



@csrf_exempt
def submit_quiz(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received JSON data:", data)  # Debug log
            answers = data.get("answers", {})
            if not answers:
                return JsonResponse({"error": "No answers provided"}, status=400)

            # Practice va savollarni olish
            practice = get_object_or_404(Practice, id=pk)
            questions = Module_3_Question.objects.filter(module__practice=practice)

            if not questions.exists():
                return JsonResponse({"error": "No questions found"}, status=404)

            # Javoblarni tekshirish
            score = 0
            for question, user_answer in zip(questions, answers.values()):
                if user_answer == question.option_select_answer:
                    score += 1

            # Sertifikatni yangilash yoki yaratish
            certificate, created = Certificate.objects.get_or_create(
                practice=practice,
                user=request.user,
                defaults={
                    'math': 0,
                    'overall': 0,
                }
            )

            certificate.math = score
            certificate.overall = certificate.english + certificate.math
            certificate.save()

            return JsonResponse({"message": "Quiz submitted successfully", "score": score})

        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)  # Debug log
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except Exception as e:
            print(f"Unexpected error: {e}")  # Debug log
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def wait3(request, pk):
    user_agent = get_user_agent(request)

    if user_agent.is_pc or user_agent.is_tablet:
        return render(request, 'time/3.html', {'id': pk})
    
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Agar mobil yoki boshqa qurilma bo'lsa