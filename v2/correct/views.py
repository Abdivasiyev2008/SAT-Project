from module_1.models import *
from module_2.models import *
from module_3.models import *
from module_4.models import *
from correct.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from certificate.models import Certificate, Checking
from django_user_agents.utils import get_user_agent
from correct.models import *

@login_required
def module_1_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Sertifikatni tekshirish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module1')

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_1_questions = Module_1_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if not module_1_questions.exists():
            return render(request, 'answers/modules/module1.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_1_questions,
            'total_questions': module_1_questions.count(),
            'question_explanations': [question.explanation for question in module_1_questions]

        }
        
        return render(request, 'answers/modules/module1.html', context)

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")


@login_required
def module_2_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Sertifikatni tekshirish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module2')

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_2_questions = Module_2_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if not module_2_questions.exists():
            return render(request, 'answers/modules/module2.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_2_questions,
            'total_questions': module_2_questions.count(),
        }
        
        return render(request, 'answers/modules/module2.html', context)

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")




@login_required
def module_3_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Sertifikatni tekshirish
    certificate_data = Certificate.objects.filter(practice=practice, user=request.user).values('module3')

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_3_questions = Module_3_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if not module_3_questions.exists():
            return render(request, 'answers/modules/module3.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_3_questions,
            'total_questions': module_3_questions.count(),
        }
        
        return render(request, 'answers/modules/module3.html', context)

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")



@login_required
def module_4_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_4_questions = Module_4_Question.objects.filter(module__practice=practice)
        check = Checking.objects.filter(practice=practice, user=request.user)

        if not module_4_questions.exists():
            return render(request, 'answers/modules/module4.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_4_questions,
            'total_questions': module_4_questions.count(),
        }
        
        return render(request, 'answers/modules/module4.html', context)

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")
