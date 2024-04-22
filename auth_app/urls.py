from .views import SocialLogin
from django.urls import path

urlpatterns = [
    path('social_login/', SocialLogin.as_view(), name='social_login'),
]
