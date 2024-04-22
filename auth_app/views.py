from .utils.providers import GetGoogleUserInfo

from django.contrib.auth import get_user_model
from core.utils.jwt import CustomAccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status

User = get_user_model()

class SocialLogin(APIView):
    def post(self, request):
        token = request.data.get('token')
        provider = request.data.get('provider')

        try:
            if provider == 'google':
                userid, email = GetGoogleUserInfo(token)
            else:
                return Response({'status': 'error', 'message': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=email, defaults={'unique_id': userid, 'provider': provider})
            user.last_login = timezone.localtime(timezone.now())
            user.save(update_fields=['last_login'])

            access_token = CustomAccessToken(user)

            return Response({
                'status': 'created successfully' if created else 'user already exists',
                'user_id': userid,
                'email': email,
                'last_login': user.last_login.isoformat(),
                'access_token': str(access_token),
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
