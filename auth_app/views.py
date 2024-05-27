from auth_app.utils.providers import get_google_user_info
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

        if not token or not provider:
            return Response({'status': 'error', 'message': 'Token and provider are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if provider == 'google':
                userid, email, photo_url = get_google_user_info(token)
            else:
                return Response({'status': 'error', 'message': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=email, defaults={'unique_id': userid, 'provider': provider, 'photo_url':photo_url})
            user.last_login = timezone.localtime(timezone.now())
            user.save(update_fields=['last_login'])

            access_token = CustomAccessToken(user)

            return Response({
                'status': 'created successfully' if created else 'user already exists',
                'user_id': userid,
                'email': email,
                'photo_url':photo_url,
                'last_login': user.last_login.isoformat(),
                'access_token': str(access_token),
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            print(str(e))
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({'status': 'error', 'message': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
