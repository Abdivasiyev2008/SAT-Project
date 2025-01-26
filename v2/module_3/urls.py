from .views import module_3_Detail, submit_quiz, wait3, save_time
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/3/', module_3_Detail, name='module_3'),
    path('submit-quiz/<int:pk>/module/3/', submit_quiz, name='submit_answers_module_3'),
    path('wait/3/<int:pk>/', wait3, name='wait3'),
    path('save-time/3/<int:pk>/', save_time, name='save_time_3'),
    
]