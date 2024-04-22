from django.urls import path, include

urlpatterns = [
    path('auth/', include('auth_app.urls')),
    path('service/', include('service.urls')),
    path('support/', include('support.urls')),
    path('users/', include('users.urls')),
]
