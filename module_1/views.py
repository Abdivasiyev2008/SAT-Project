from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Module_1, Module_1_Question, Practice
from certificate.models import Certificate, Checking
from django.contrib.auth.decorators import login_required

@login_required
def module_1_Detail(request, pk):
    # Retrieve the Practice object or return a 404 if not found
    practice = get_object_or_404(Practice, id=pk)
    
    # Retrieve the questions related to the practice
    module_1_questions = Module_1_Question.objects.filter(module__practice=practice)
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user)
    check = Checking.objects.filter(practice=practice, user=request.user)

    if check.exists():
        return redirect(f'/tests/{pk}/certificate/get')

    else:
        # If there are no questions
        if not module_1_questions.exists():
            return render(request, 'modules/module_1.html', {'message': 'No questions available for this test.'})

        # Prepare context to pass to template
        context = {
            'practice': practice,
            'questions': module_1_questions  # Pass the filtered questions
        }

        return render(request, 'modules/module_1.html', context)

def submit_quiz(request, pk):
    if request.method == "POST":
        try:
            # Get practice.id from the URL (pk)
            practice_id = pk
            data = json.loads(request.body)  # Parse the incoming JSON data
            answers = data.get("answers", {})  # Extract answers from the request
            
            if not answers:
                return JsonResponse({"error": "No answers provided"}, status=400)

            # Fetch the practice object
            try:
                practice = Practice.objects.get(id=practice_id)

            except Practice.DoesNotExist:
                return JsonResponse({"error": "Practice not found"}, status=404)

            # Fetch all questions related to the practice
            module_questions = Module_1_Question.objects.filter(module__practice=practice)
            all_answers = []
            score = 0

            if not module_questions.exists():
                return JsonResponse({"error": "No questions found for this practice"}, status=404)

            # Loop over the questions and check if answers are correct
            for i in list(answers.keys()):
                if i == "" or i == " ":
                    all_answers.append(' ')
                
                else:
                    all_answers.append(answers.get(i))

            for question, user_answer in zip(module_questions, all_answers):
                if user_answer == question.option_select_answer:
                    score += 1

            # Check if the user already has a certificate for this practice
            try:
                certificate = Certificate.objects.get(user=request.user, practice=practice)

                # If certificate exists, update the score
                certificate.english += score
                certificate.overall = certificate.english  # You may want to update the overall score too
                certificate.save()
                
            except Certificate.DoesNotExist:
                # If no certificate exists for the user, create a new one
                Certificate.objects.create(
                    practice=practice,
                    user=request.user,
                    english=score,
                    math=0,
                    overall=score,
                )

            return JsonResponse({})

        except json.JSONDecodeError:
            # If the incoming data is not valid JSON, return an error response
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except Exception as e:
            # If any other error occurs, catch it and return a generic error response
            print(f"Error: {e}")  # Optionally log the error for debugging
            return JsonResponse({"error": "An error occurred while processing your request."}, status=500)

    else:
        # If the request method is not POST, return an error response
        return JsonResponse({"error": "Invalid request method"}, status=405)
