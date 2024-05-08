from .views import DeleteUser
from django.urls import path

urlpatterns = [
    path('delete-user/', DeleteUser.as_view(), name='delete-user'),
]
