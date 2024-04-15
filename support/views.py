from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.tokens import AccessToken
from .utils.mail_sender import send_mail_to_support
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils.jwt import HasAPIAccess
from rest_framework import status

class HaveAProblem(APIView):
    permission_classes = [HasAPIAccess]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:

            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != b'bearer':
                return Response({'detail': 'Missing JWT'}, status=status.HTTP_400_BAD_REQUEST)

            access_token = auth[1].decode('utf-8')
            decoded_token = AccessToken(access_token)

            email = decoded_token['email']
            mail_subject = request.data.get('mail_subject')
            mail_content = request.data.get('mail_content')

            if not all([access_token, email, mail_subject, mail_content]):
                return Response({'detail': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

            send_mail_to_support(mail_subject, mail_content, email)
            return Response({'detail': 'Mail sent'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
