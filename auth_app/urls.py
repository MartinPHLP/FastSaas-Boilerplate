from .views import SocialLogin
from django.urls import path

urlpatterns = [
    path('social-login/', SocialLogin.as_view(), name='social-login'),
]
