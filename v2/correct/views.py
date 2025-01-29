from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from module_1.models import *
from module_2.models import *
from module_3.models import *
from module_4.models import *
from correct.models import *
from django_user_agents.utils import get_user_agent


@login_required
def module_1_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_1_questions = Module_1_Question.objects.filter(module__practice=practice)

        # Answerlarni olish
        module_1_answers = Answer1.objects.filter(module1_ans__practice=practice)

        # Prepare data for the template
        if not module_1_questions.exists():
            return render(request, 'answers/modules/module1.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_1_questions,
            'answers_data': module_1_answers,
            'id': practice.id,
        }
        return render(request, 'answers/modules/module1.html', context)

    else:
        # pk ni jonatish
        return HttpResponse(f"If you want to use this platform, please use a computer. Your practice ID is: {pk}")


@login_required
def module_2_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_2_questions = Module_2_Question.objects.filter(module__practice=practice)

        # Answerlarni olish
        module_2_answers = Answer2.objects.filter(module2_ans__practice=practice)

        # Prepare data for the template
        if not module_2_questions.exists():
            return render(request, 'answers/modules/module2.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_2_questions,
            'answers_data': module_2_answers,
            'id': practice.id,
        }
        return render(request, 'answers/modules/module2.html', context)

    else:
        # pk ni jonatish
        return HttpResponse(f"If you want to use this platform, please use a computer. Your practice ID is: {pk}")




@login_required
def module_3_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_3_questions = Module_3_Question.objects.filter(module__practice=practice)

        # Answerlarni olish
        module_3_answers = Answer3.objects.filter(module3_ans__practice=practice)

        # Prepare data for the template
        if not module_3_questions.exists():
            return render(request, 'answers/modules/module3.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_3_questions,
            'answers_data': module_3_answers,
            'id': practice.id,
        }
        return render(request, 'answers/modules/module3.html', context)

    else:
        # pk ni jonatish
        return HttpResponse(f"If you want to use this platform, please use a computer. Your practice ID is: {pk}")



@login_required
def module_4_Detail(request, pk):
    user_agent = get_user_agent(request)

    # Practice obyektini olish
    practice = get_object_or_404(Practice, id=pk)

    # Faqat PC yoki planshetdan kirish
    if user_agent.is_pc or user_agent.is_tablet:
        module_4_questions = Module_4_Question.objects.filter(module__practice=practice)

        # Answerlarni olish
        module_4_answers = Answer4.objects.filter(module4_ans__practice=practice)

        # Prepare data for the template
        if not module_4_questions.exists():
            return render(request, 'answers/modules/module4.html', {'message': 'No questions available for this test.'})

        context = {
            'practice': practice,
            'questions': module_4_questions,
            'answers_data': module_4_answers,
            'id': practice.id,
        }
        return render(request, 'answers/modules/module4.html', context)

    else:
        # pk ni jonatish
        return HttpResponse(f"If you want to use this platform, please use a computer. Your practice ID is: {pk}")
