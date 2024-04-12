from .views import GenerationView
from django.urls import path

urlpatterns = [
    path('generate/', GenerationView.as_view(), name='generate')
]
