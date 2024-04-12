from core.utils.jwt import CustomAccessToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from google.auth.transport import requests
from rest_framework.views import APIView
from google.oauth2 import id_token
from django.utils import timezone
from rest_framework import status
from dotenv import load_dotenv
import os

load_dotenv()

User = get_user_model()

class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get('token')
        CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            userid = idinfo['sub']
            email = idinfo.get('email')

            user, created = User.objects.get_or_create(email=email, defaults={'unique_id': userid, 'provider': "google"})
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
