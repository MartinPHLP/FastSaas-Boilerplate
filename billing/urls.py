from django.urls import path
from . import views

urlpatterns = [
    path('webhook-listener/', views.PayPalWebhookListener.as_view(), name='webhook-listener'),
    path('post-sub-id/', views.PostSubId.as_view(), name='post-sub-id'),
]
