from .views import module_3_Detail, submit_quiz
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/3/', module_3_Detail, name='module_3'),
    path('submit-quiz/<int:pk>/module/3/', submit_quiz, name='submit_answers_module_3'),
    
]