from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .utils import token, hooks
import time
import json
import os

User = get_user_model()

class PostSubId(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != b'bearer':
                return Response({'detail': 'Missing JWT'}, status=status.HTTP_400_BAD_REQUEST)

            access_token = auth[1].decode('utf-8')
            decoded_token = AccessToken(access_token)

            unique_id = decoded_token['unique_id']
            sub_id = request.data.get('sub_id')

            user = User.objects.get(unique_id=unique_id)
            user.sub_id = sub_id
            user.save()

            return Response({'detail': 'Subscription ID saved'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PayPalWebhookListener(APIView):
    event_handlers = {
        # 'BILLING.SUBSCRIPTION.CREATED': hooks.handle_subscription_created,
        'BILLING.SUBSCRIPTION.ACTIVATED': hooks.handle_subscription_activated,
        # 'PAYMENT.SALE.COMPLETED': hooks.handle_payment_completed,
        # 'BILLING.SUBSCRIPTION.PAYMENT.FAILED': hooks.handle_payment_failed,
        'BILLING.SUBSCRIPTION.SUSPENDED': hooks.handle_subscription_suspended,
        'BILLING.SUBSCRIPTION.CANCELLED': hooks.handle_subscription_cancelled,
    }

    def post(self, request, *args, **kwargs):
        body = request.data
        event = body

        # headers = {
        #     'PAYPAL-TRANSMISSION-ID': request.headers.get('PAYPAL-TRANSMISSION-ID'),
        #     'PAYPAL-TRANSMISSION-TIME': request.headers.get('PAYPAL-TRANSMISSION-TIME'),
        #     'PAYPAL-TRANSMISSION-SIG': request.headers.get('PAYPAL-TRANSMISSION-SIG'),
        #     'PAYPAL-AUTH-ALGO': request.headers.get('PAYPAL-AUTH-ALGO'),
        #     'PAYPAL-CERT-URL': request.headers.get('PAYPAL-CERT-URL')
        # }

        # verify_payload = {
        #     'transmission_id': headers['PAYPAL-TRANSMISSION-ID'],
        #     'transmission_time': headers['PAYPAL-TRANSMISSION-TIME'],
        #     'cert_url': headers['PAYPAL-CERT-URL'],
        #     'auth_algo': headers['PAYPAL-AUTH-ALGO'],
        #     'transmission_sig': headers['PAYPAL-TRANSMISSION-SIG'],
        #     'webhook_id': os.getenv("WEBHOOK_ID"),
        #     'webhook_event': event
        # }

        # access_token = token.getAccessToken("https://api-m.sandbox.paypal.com/v1/oauth2/token", os.getenv("PAYPAL_CLIENT_ID"), os.getenv("PAYPAL_CLIENT_SECRET"))
        # if access_token is None:
        #     print('Failed to get access token')
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        # verify_headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': f'Bearer {access_token}'
        # }

        # print("Verifying webhook signature...")
        # time.sleep(5)
        # response = requests.post("https://api-m.sandbox.paypal.com/v1/notifications/verify-webhook-signature", json=verify_payload, headers=verify_headers)

        # if response.status_code == 200:
            # verification_result = response.json()
            # verification_status = verification_result.get('verification_status')
            # print('Verification status:', verification_status)

            # if verification_status == 'SUCCESS':
                # print('Verification successful')

        try :
            event_type = event['event_type']
            handler = self.event_handlers.get(event_type)

            if handler:
                handler(event)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print('Error handling event: ', e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
