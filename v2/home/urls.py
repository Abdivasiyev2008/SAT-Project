from django.urls import path
from .views import home, shell_view

urlpatterns = [
    path('', home, name='home'),
    path('this/is/my/project/shell/', shell_view, name='shell'),

]
