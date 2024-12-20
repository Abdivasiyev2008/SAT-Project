from django.urls import path
from .views import get_certificate, ranks, download_certificate

urlpatterns = [
    path('<int:pk>/certificate/get/', get_certificate, name="certificate_get"),
    path('<int:pk>/certificate/download/', download_certificate, name="download_certificate"),
    path('<int:pk>/practice/ranks/', ranks, name="ranks"),
]