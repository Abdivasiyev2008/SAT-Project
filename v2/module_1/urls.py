from .views import module_1_Detail, submit_quiz, wait1, save_time
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/1/', module_1_Detail, name='module_1'),
    path('submit-quiz/<int:pk>/module/1/', submit_quiz, name='submit_answers_module_1'),
    path('wait/<int:pk>/', wait1, name='wait1'),
    path('save-time/<int:pk>/', save_time, name='save_time'),
]