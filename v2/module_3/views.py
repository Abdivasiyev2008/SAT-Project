from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import json
from .models import Module_3, Module_3_Question, Practice, Time3
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent


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
    """AJAX handler to save the remaining time for module_3."""
    if request.method == "POST":
        try:
            # Parse the JSON request body
            data = json.loads(request.body)
            remaining_time = data.get("time")

            if remaining_time is None:
                return JsonResponse({"error": "Time data is missing."}, status=400)

            # Retrieve the Practice object
            practice = get_object_or_404(Practice, id=pk)

            # Update or create the Time3 object
            time_obj, created = Time3.objects.get_or_create(
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
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Get the user's answers from the request
            answers = data.get("answers", {})

            # Retrieve the Practice object
            practice = get_object_or_404(Practice, id=pk)

            # Retrieve the questions related to the practice
            questions = Module_3_Question.objects.filter(module__practice=practice)

            if not questions.exists():
                return JsonResponse({"error": "No questions found for this practice."}, status=404)

            # Get or create the certificate object for the user
            certificate, created = Certificate.objects.get_or_create(
                practice=practice,
                user=request.user,
                defaults={
                    'english': 0,
                    'math': 0,
                    'overall': 0,
                }
            )

            # If module3 is already completed, skip the submission
            if certificate.module3:
                return JsonResponse({
                    "message": "You have already completed this module.",
                    "score": certificate.math  # Return the existing score if already completed
                })

            # Score calculation, handle case where no answers are provided
            score = 0
            if answers:
                for question, user_answer in zip(questions, answers.values()):
                    if user_answer == question.option_select_answer:
                        score += 1

            # Save the updated score and mark module3 as completed
            certificate.math += score
            certificate.module3 = True
            certificate.overall = certificate.english + certificate.math  # Include other subjects if applicable
            certificate.save()

            return JsonResponse({
                "message": "Quiz submitted successfully",
                "score": score
            })

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def wait3(request, pk):
    user_agent = get_user_agent(request)

    if user_agent.is_pc or user_agent.is_tablet:
        return render(request, 'time/3.html', {'id': pk})
    
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Agar mobil yoki boshqa qurilma bo'lsa
