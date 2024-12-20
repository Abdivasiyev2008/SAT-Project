from .views import module_1_Detail, submit_quiz
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/1/', module_1_Detail, name='module_1'),
    path('submit-quiz/<int:pk>/module/1/', submit_quiz, name='submit_answers_module_1'),
]
