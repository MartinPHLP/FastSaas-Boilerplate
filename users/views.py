from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()

class DeleteUser(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return Response({'detail': 'Missing JWT'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = auth[1].decode('utf-8')
        decoded_token = AccessToken(access_token)

        unique_id = decoded_token['unique_id']
        user = User.objects.get(unique_id=unique_id)
        try:
            user.delete()
            return Response({'status': 'deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
