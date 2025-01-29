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
from correct.models import *

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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            answers = data.get("answers", {})
            print("User Answers:", answers)  # Foydalanuvchi javoblarini konsolga chiqarish
            practice = get_object_or_404(Practice, id=pk)

            # Module 4 savollarini olish
            questions = Module_4_Question.objects.filter(module__practice=practice)
            if not questions.exists():
                return JsonResponse({"error": "No questions found for this practice."}, status=404)

            with transaction.atomic():
                # Sertifikatni olish yoki yaratish
                certificate, created = Certificate.objects.get_or_create(
                    practice=practice,
                    user=request.user,
                    defaults={'english': 0, 'math': 0, 'overall': 0}
                )

                # Agar modul 4 allaqachon tugallangan bo'lsa
                if certificate.module4:
                    return JsonResponse({
                        "message": "You have already completed this module.",
                        "score": certificate.math  # Modul 4 uchun mavjud ballni qaytarish
                    })

                score = 0
                module4_ans = Module4_Ans.objects.create(  # Modul 4 uchun javoblar saqlash
                    user=request.user,
                    practice=practice
                )

                # Savollarni tekshirish va foydalanuvchi javoblarini solishtirish
                for idx, question in enumerate(questions):
                    user_answer = answers.get(str(idx))  # Foydalanuvchi javobini olish

                    if user_answer == question.option_a:
                        user_answer = question.option_a
                    
                    elif user_answer == question.option_b:
                        user_answer = question.option_b
                    
                    elif user_answer == question.option_c:
                        user_answer = question.option_c

                    elif user_answer == question.option_d:
                        user_answer = question.option_d

                    elif user_answer == question.option_input_answer:
                        user_answer = question.option_input_answer

                    correct_answer = ""

                    # Agar foydalanuvchi javob bergan bo'lsa
                    if user_answer:
                        if user_answer == question.option_select_answer or user_answer == question.option_input_answer:
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

                    else:
                        select = question.option_input_answer

                    # Javobni Answer4 modeliga saqlash
                    Answer4.objects.get_or_create(  # Answer4 modelini ishlatish
                        module4_ans=module4_ans,
                        user_answer=user_answer,
                        correct_answer=select,  # To'g'ri javobni saqlash
                        question=question.question
                    )

                # Hisob-kitob va scaled scoreni qo'shish
                certificate.math += score
                certificate.math = int(calculate_scaled_score(certificate.math))
                certificate.english = int(get_scaled_score(certificate.english))
                certificate.module4 = True  # Modul 4 tugallangan deb belgilash
                certificate.overall = certificate.english + certificate.math  # Umumiy ballni hisoblash
                certificate.save()  # Sertifikatni saqlash

            return JsonResponse({
                "message": "Quiz submitted successfully",
                "score": certificate.overall,  # Xususiy bal
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
