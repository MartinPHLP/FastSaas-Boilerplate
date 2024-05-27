from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('unique_id', 'sub_id', 'photo_url', 'provider', 'api_access')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('unique_id', 'provider', 'api_access')}),
    )
    list_display = ('email', 'username', 'unique_id', 'provider', 'is_staff', 'api_access', 'photo_url')  # Ajoutez 'photo_url' ici
    search_fields = ('email', 'username', 'unique_id')

admin.site.register(CustomUser, CustomUserAdmin)
