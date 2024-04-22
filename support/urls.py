from .views import HaveAProblem, ContactSupport
from django.urls import path

urlpatterns = [
    path('contact_support/', ContactSupport.as_view(), name='contact_support'),
    path('have_a_problem/', HaveAProblem.as_view(), name='have_a_problem')
]
