from django.urls import path
from .views import search_form, stats

urlpatterns = [
    path('v1/search/', search_form, name='search_form'),
    path('v1/stats/', stats, name='stats'),
    # boshqa URL'lar
]
