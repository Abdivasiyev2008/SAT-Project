from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Module_1_Question, Practice, Time1  # Module_2 -> Module_1
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent
from django.utils.timezone import now
import datetime
from django.db import transaction
from correct.models import *

@login_required
def module_1_Detail(request, pk):  # module_2_Detail -> module_1_Detail
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Sertifikatni tekshirish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module1')  # module2 -> module1
    if certificate_data.exists() and certificate_data[0]['module1']:  # module2 -> module1
        return redirect(f'/tests/practice/{pk}/3/')  # module1 uchun 3-raqamga yo'naltirish

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_1_questions = Module_1_Question.objects.filter(module__practice=practice)  # Module_2_Question -> Module_1_Question
        check = Checking.objects.filter(practice=practice, user=request.user)

        if check.exists():
            return redirect(f'/tests/{pk}/certificate/get')

        if not module_1_questions.exists():
            return render(request, 'modules/module_1.html', {'message': 'No questions available for this test.'})  # module_2.html -> module_1.html

        # Timer uchun vaqtni olish yoki yangisini yaratish
        time_obj, created = Time1.objects.get_or_create(
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
            'questions': module_1_questions,  # module_2_questions -> module_1_questions
            'total_questions': module_1_questions.count(),  # module_2_questions.count() -> module_1_questions.count()
            'remaining_time': remaining_time,  # Timer uchun qoldiq vaqt
        }
        return render(request, 'modules/module_1.html', context)  # module_2.html -> module_1.html

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
            time_obj, created = Time1.objects.get_or_create(
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
            answers = data.get("answers", {})

            if not answers:
                return JsonResponse({"error": "No answers provided."}, status=400)

            # Practice va savollarni olish
            practice = get_object_or_404(Practice, id=pk)
            questions = Module_1_Question.objects.filter(module__practice=practice)  # Module_2_Question -> Module_1_Question

            if not questions.exists():
                return JsonResponse({"error": "No questions found"}, status=404)

            # Javoblarni tekshirish
            score = 0
            for question, user_answer in zip(questions, answers.values()):
                if user_answer == question.option_select_answer:
                    score += 1

            # Sertifikatni olish yoki yaratish
            certificates = Certificate.objects.filter(practice=practice, user=request.user)

            if certificates.exists():
                certificate = certificates.latest('id')  # Eng yangi sertifikatni olish
                certificates.exclude(id=certificate.id).delete()  # Eskilarini o‘chirish
            else:
                certificate = Certificate.objects.create(
                    practice=practice,
                    user=request.user,
                    english=0,
                    math=0,
                    overall=0,
                )
            
            if certificate.module1 == True:  # module2 -> module1
                pass
            else:
                # Sertifikatni yangilash
                certificate.english = score
                certificate.module1 = True  # module2 -> module1
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


def wait1(request, pk):
    user_agent = get_user_agent(request)
    if user_agent.is_pc or user_agent.is_tablet:
        # Time1 obyektini avtomatik yaratish
        practice = get_object_or_404(Practice, id=pk)
        Time1.objects.get_or_create(user=request.user, practice=practice, defaults={"time": 32 * 60})
        return render(request, 'time/1.html', {'id': pk})
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")
