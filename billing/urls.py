from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('create-portal-session/', views.CustomerPortal.as_view(), name='create-portal-session'),
    path('webhook/', views.WebhookReceived.as_view(), name='webhook'),
]
