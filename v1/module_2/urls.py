from .views import module_2_Detail, submit_quiz, timeBreak, save_time
from django.urls import path

urlpatterns = [
    path('practice/<int:pk>/2/', module_2_Detail, name='module_2'),
    path('practice/<int:pk>/time/break/', timeBreak, name='timeBreak'),
    path('submit-quiz/<int:pk>/module/2/', submit_quiz, name='submit_answers_module_2'),
    path('save-time/2/<int:pk>/', save_time, name='save_time_2'),
]
