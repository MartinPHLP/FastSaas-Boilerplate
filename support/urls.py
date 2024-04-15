from .views import HaveAProblem
from django.urls import path

urlpatterns = [
    path('have_a_problem/', HaveAProblem.as_view(), name='have_a_problem')
]
