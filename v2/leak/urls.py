from django.urls import path
from .views import search_api, LeakPasswordCreateView, DomainLeakCountView

urlpatterns = [
    path('v1/leak_passwords/', search_api, name='search_api'),
    path('v1/leak/create/', LeakPasswordCreateView.as_view(), name='leakpassword-create'),
    path('v1/domain/<str:domain>/', DomainLeakCountView.as_view(), name='domain-leak-count'),

]
