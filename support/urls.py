from .views import HaveAProblem, ContactSupport
from django.urls import path

urlpatterns = [
    path('contact-support/', ContactSupport.as_view(), name='contact-support'),
    path('have-a-problem/', HaveAProblem.as_view(), name='have-a-problem')
]
