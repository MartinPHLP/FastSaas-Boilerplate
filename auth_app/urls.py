from .views import GoogleLogin
from django.urls import path

urlpatterns = [
    path('google_login/', GoogleLogin.as_view(), name='google_login'),
]
