from django.shortcuts import render, get_object_or_404, redirect
from .models import Practice, HideUser, HideUserPractice
from django_user_agents.utils import get_user_agent
from django.http import HttpResponse

# Create your views here.


def practiceList(request):
    user_agent = get_user_agent(request)
    
    if user_agent.is_pc or user_agent.is_tablet:
        if request.user.is_authenticated:
            hide_user = HideUser.objects.filter(user=request.user).first()
            if hide_user:
                practices = Practice.objects.filter(
                    hidepractice__in=HideUserPractice.objects.filter(user=hide_user).values_list('practice', flat=True)
                ) | Practice.objects.filter(action=True)  # Action=True for all
            else:
                practices = Practice.objects.filter(action=True)  # Action=True for all
        else:
            practices = Practice.objects.filter(action=True)
    
        context = {
            'practice': practices.distinct()
        }
    
        return render(request, 'test/practice.html', context)
    
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Agar mobil yoki boshqa qurilma bo'lsa

def ask(request, pk):
    user_agent = get_user_agent(request)
    
    if user_agent.is_pc or user_agent.is_tablet:
        practice = Practice.objects.filter(id=pk)
        name = ""
        for i in practice:
            name = i.name
    
        return render(request, 'test/ask.html', {'id': pk, 'name': name})

    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Agar mobil yoki boshqa qurilma bo'lsa