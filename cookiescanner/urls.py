from django.urls import path
from .views import CookieScanView

urlpatterns = [
    path('api/scan/', CookieScanView.as_view(), name='cookie-scan'),
]
