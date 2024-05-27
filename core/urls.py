from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('service/', include('service.urls')),
    path('support/', include('support.urls')),
    path('users/', include('users.urls')),
    path('billing/', include('billing.urls')),
]
