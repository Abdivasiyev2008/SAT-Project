from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Module_1_Question, Practice, Time1
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent
from django.utils.timezone import now
import datetime
from django.db import transaction
from correct.models import *

@login_required
def module_1_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Sertifikatni tekshirish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module1')
    if certificate_data.exists() and certificate_data[0]['module1']:
        return redirect(f'/tests/practice/{pk}/2/')

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_1_questions = Module_1_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if check.exists():
            return redirect(f'/tests/{pk}/certificate/get')

        if not module_1_questions.exists():
            return render(request, 'modules/module_1.html', {'message': 'No questions available for this test.'})

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
            'questions': module_1_questions,
            'total_questions': module_1_questions.count(),
            'remaining_time': remaining_time,  # Timer uchun qoldiq vaqt
        }
        return render(request, 'modules/module_1.html', context)

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
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def submit_quiz(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            answers = data.get("answers", {})
            print("User Answers:", answers)  # Foydalanuvchi javoblarini konsolga chiqarish
            practice = get_object_or_404(Practice, id=pk)

            questions = Module_1_Question.objects.filter(module__practice=practice)
            if not questions.exists():
                return JsonResponse({"error": "No questions found for this practice."}, status=404)

            with transaction.atomic():
                certificate, created = Certificate.objects.get_or_create(
                    practice=practice,
                    user=request.user,
                    defaults={'english': 0, 'math': 0, 'overall': 0}
                )

                if certificate.module1:
                    return JsonResponse({
                        "message": "You have already completed this module.",
                        "score": certificate.english
                    })

                score = 0
                module1_ans = Module1_Ans.objects.create(
                    user = request.user,
                    practice = practice
                )

                # Answers keylarni tekshirib, noto'g'ri javoblarni tekshirayotganini nazorat qilish
                for idx, question in enumerate(questions):
                    user_answer = answers.get(str(idx))  # user_answer = answers.get(str(idx)) ning xavfsiz usuli
                    if user_answer == question.option_a:
                        user_answer = question.option_a
                    
                    elif user_answer == question.option_b:
                        user_answer = question.option_b
                    
                    elif user_answer == question.option_c:
                        user_answer = question.option_c

                    elif user_answer == question.option_d:
                        user_answer = question.option_d

                    # Agar foydalanuvchi javob bermagan bo'lsa, user_answer None bo'ladi
                    if user_answer:
                        if user_answer == question.option_select_answer:
                            score += 1
                    else:
                        # Foydalanuvchi javob bermagan bo'lsa, `null` saqlaymiz
                        user_answer = None
                    
                    select = ""
                    
                    if question.option_select_answer == question.option_a:
                        select = question.option_a
                    
                    elif question.option_select_answer == question.option_b:
                        select = question.option_b
                    
                    elif question.option_select_answer == question.option_c:
                        select = question.option_c

                    elif question.option_select_answer == question.option_d:
                        select = question.option_d

                    Answer1.objects.get_or_create(
                        module1_ans=module1_ans,
                        user_answer=user_answer,
                        correct_answer=question.option_select_answer,  # To'g'ri javobni saqlaymiz
                        question=select
                    )

                certificate.english += score
                certificate.module1 = True
                certificate.overall = certificate.english + certificate.math
                certificate.save()

            return JsonResponse({
                "message": "Quiz submitted successfully",
                "score": score,
                "total_questions": questions.count(),
                "answered_questions": len(answers),
            })

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Xatolikni konsolga chiqarish
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


def wait1(request, pk):
    user_agent = get_user_agent(request)
    if user_agent.is_pc or user_agent.is_tablet:
        # Time1 obyektini avtomatik yaratish
        practice = get_object_or_404(Practice, id=pk)
        Time1.objects.get_or_create(user=request.user, practice=practice, defaults={"time": 32 * 60})
        return render(request, 'time/1.html', {'id': pk})
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")

