from django.urls import path
from .views import practiceList

urlpatterns = [
    path('practice/', practiceList, name='practice'),
]