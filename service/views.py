from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.views import APIView
from core.utils.jwt import HasAPIAccess
from rest_framework import status
import requests

class GenerationView(APIView):
    permission_classes = [HasAPIAccess]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return Response({'detail': 'Missing JWT'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = auth[1].decode('utf-8')
        mail_type = request.data.get('mail_type')
        customer = request.data.get('customer')
        promo = request.data.get('promo')
        link = request.data.get('link')
        infos = request.data.get('infos')

        if not all([access_token, mail_type, customer, promo, link, infos]):
            return Response({'detail': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        data = {
            'mail_type': mail_type,
            'customer': customer,
            'promo': promo,
            'link': link,
            'infos': infos
        }
        response = requests.post('http://localhost:5000/api_generation', headers=headers, json=data)

        if response.status_code != 200:
            return Response({'detail': 'Microservice request failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response.json(), status=status.HTTP_200_OK)
