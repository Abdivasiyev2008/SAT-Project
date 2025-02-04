from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now  # Import this
import json, datetime
from .models import Module_2, Module_2_Question, Practice, Time2  # Ensure Time1 is included
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent
from django.db import transaction
from correct.models import *

@login_required
def module_2_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Retrieve the Practice object or return a 404 if not found
    practice = get_object_or_404(Practice, id=pk)

    # Check if the user has completed this module
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module2')
    
    if certificate_data.exists():
        module2_value = certificate_data[0]['module2']
        if module2_value:  # If module2 is already completed, redirect to next module
            return redirect(f'/tests/practice/{pk}/3/')
    
    # Handle requests only from PC or tablet
    if user_agent.is_pc or user_agent.is_tablet:
        # Retrieve the questions related to the practice
        module_2_questions = Module_2_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if check.exists():
            return redirect(f'/tests/{pk}/certificate/get')

        # If no questions are available, show a message
        if not module_2_questions.exists():
            return render(request, 'modules/module_2.html', {'message': 'No questions available for this test.'})

        # Timer functionality: Retrieve or create a Time2 object for the user
        time_obj, created = Time2.objects.get_or_create(
            user=request.user,
            practice=practice,
            defaults={"time": 32 * 60}  # Default time set to 32 minutes
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
            'questions': module_2_questions,
            'total_questions': module_2_questions.count(),  # Total number of questions
            'remaining_time': remaining_time,  # Timer for the module
        }
        
        return render(request, 'modules/module_2.html', context)
    
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Handle non-PC devices


@csrf_exempt
def save_time(request, pk):
    """AJAX handler to save the remaining time for module_2."""
    if request.method == "POST":
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            remaining_time = data.get("time")

            if remaining_time is None:
                return JsonResponse({"error": "Time data is missing."}, status=400)

            # Retrieve the Practice object
            practice = get_object_or_404(Practice, id=pk)

            # Update or create the Time2 object
            time_obj, created = Time2.objects.get_or_create(
                user=request.user,
                practice=practice,
                defaults={"time": remaining_time}
            )

            if not created:
                # Update time and mark the timestamp
                time_obj.time = remaining_time
                time_obj.updated_at = now()
                time_obj.save()

            return JsonResponse({"message": "Time saved successfully.", "remaining_time": time_obj.time})

        except Exception as e:
            # Return error response in case of unexpected issues
            return JsonResponse({"error": str(e)}, status=400)

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
            questions = Module_2_Question.objects.filter(module__practice=practice)

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
                    'english': 0,
                    'math': 0,
                    'overall': 0,
                }
            )

            certificate.english += score
            certificate.module2 = True
            certificate.overall = certificate.english
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

def timeBreak(request, pk):
    return render(request, 'time/break.html', {'id': pk})
