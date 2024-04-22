from .views import DeleteUser
from django.urls import path

urlpatterns = [
    path('delete_user/', DeleteUser.as_view(), name='delete_user'),
]
