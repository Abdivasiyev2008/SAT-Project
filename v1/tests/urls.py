from django.urls import path
from .views import practiceList, ask

urlpatterns = [
    path('practice/', practiceList, name='practice'),
    path('practice/<int:pk>/', ask, name='ask'),
]