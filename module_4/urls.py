from .views import module_4_Detail, submit_quiz
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/4/', module_4_Detail, name='module_4'),
    path('submit-quiz/<int:pk>/module/4/', submit_quiz, name='submit_answers_module_4'),
    
]