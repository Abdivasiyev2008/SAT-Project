from django.shortcuts import render, get_object_or_404, redirect
from .models import Practice, HideUser, HideUserPractice

# Create your views here.


def practiceList(request):
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

def ask(request, pk):
    practice = Practice.objects.filter(id=pk)
    name = ""
    for i in practice:
        name = i.name

    return render(request, 'test/ask.html', {'id': pk, 'name': name})