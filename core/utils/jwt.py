from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class CustomAccessToken(AccessToken):
    token_type = 'access'

    def __init__(self, user):
        super().__init__()

        self['user_id'] = user.id
        self['email'] = user.email
        self['unique_id'] = user.unique_id
        self['provider'] = user.provider
        self['api_access'] = user.api_access
        self['is_staff'] = user.is_staff

class HasAPIAccess(BasePermission):
    """Only allows users with api_access = True."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('User is not authenticated')
        if not getattr(request.user, 'api_access', False):
            raise PermissionDenied('User does not have API access')
        return True

class IsStaffUser(BasePermission):
    """Only allows users with is_staff = True."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise PermissionDenied('User is not authenticated')
        if not getattr(request.user, 'is_staff', False):
            raise PermissionDenied('User is not a staff member')
        return True
