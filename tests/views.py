from django.shortcuts import render, get_object_or_404
from .models import Practice

# Create your views here.


def practiceList(request):
    practice = Practice.objects.all()

    context = {
        'practice': practice
    }

    return render(request, 'test/practice.html', context)
