from django.shortcuts import render
from django.http import HttpResponse
from django_user_agents.utils import get_user_agent

def home(request):
    user_agent = get_user_agent(request)

    # Qurilma kompyuter ekanligini tekshiramiz
    if user_agent.is_pc or user_agent.is_tablet:
        return render(request, 'home.html')  # Kompyuter bo'lsa home.html sahifasiga o'tadi
    else:
        return HttpResponse("If you want to use this platform, please use a computer.")  # Agar mobil yoki boshqa qurilma bo'lsa
