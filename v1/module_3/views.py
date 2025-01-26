from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Module_3, Module_3_Question, Practice
from certificate.models import Certificate, Checking


def module_3_Detail(request, pk):
    # Retrieve the Practice object or return a 404 if not found
    practice = get_object_or_404(Practice, id=pk)
    
    # Retrieve the questions related to the practice
    module_3_questions = Module_3_Question.objects.filter(module__practice=practice)

    certificate_data = Certificate.objects.filter(practice=practice, user=request.user)
    check = Checking.objects.filter(practice=practice, user=request.user)

    if check.exists():
        return redirect(f'/tests/{pk}/certificate/get')
    
    else:
        if not module_3_questions.exists():
            return render(request, 'modules/module_3.html', {'message': 'No questions available for this test.'})

        # Prepare context to pass to template
        context = {
            'practice': practice,
            'questions': module_3_questions  # Pass the filtered questions
    }

    return render(request, 'modules/module_3.html', context)



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
