from correct.views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>/1/', module_1_Detail, name='answer_module_1'),
    path('<int:pk>/2/', module_2_Detail, name='answer_module_2'),
    path('<int:pk>/3/', module_3_Detail, name='answer_module_3'),
    path('<int:pk>/4/', module_4_Detail, name='answer_module_4'),
]