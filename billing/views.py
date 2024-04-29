from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.conf import settings
import stripe
import os

# Configurez votre clé d'API Stripe ici.
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class CreateCheckoutSession(APIView):
    """
    Cette vue est responsable de créer une session de paiement Stripe.
    """
    def post(self, request):
        try:
            # Récupère les données de la requête
            lookup_key = request.data.get('lookup_key')

            # Récupère le prix correspondant au lookup_key
            prices = stripe.Price.list(
                lookup_keys=[lookup_key],
                expand=['data.product']
            )

            # Crée une session de paiement Stripe
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=f"{settings.YOUR_DOMAIN}?success=true&session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.YOUR_DOMAIN}?canceled=true",
            )

            # Redirige l'utilisateur vers la session de paiement Stripe
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            # Gère les erreurs
            print(e)
            return Response({"error": "Erreur lors de la création de la session de paiement"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerPortal(APIView):
    """
    Cette vue est responsable de créer une session de portail client pour gérer les abonnements.
    """
    def post(self, request):
        # Récupère l'ID de la session de paiement depuis la requête
        checkout_session_id = request.data.get('session_id')

        # Récupère la session de paiement Stripe
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        # Crée une session de portail client pour gérer l'abonnement
        portal_session = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=settings.YOUR_DOMAIN,
        )

        # Redirige l'utilisateur vers la session de portail client
        return redirect(portal_session.url, code=303)

class WebhookReceived(APIView):
    """
    Cette vue est responsable de gérer les événements webhook Stripe.
    """
    def post(self, request):
        # Remplacez par votre secret de webhook unique
        webhook_secret = 'whsec_12345'

        request_data = request.body

        try:
            # Vérifie la signature du webhook
            signature = request.headers.get('stripe-signature')
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenez les données de l'événement et le type d'événement
        data = event['data']
        event_type = event['type']
        data_object = data['object']

        print(f'Event: {event_type}')

        # Traite les événements spécifiques
        if event_type == 'checkout.session.completed':
            print('🔔 Paiement réussi !')
        elif event_type == 'customer.subscription.trial_will_end':
            print('La période d\'essai de l\'abonnement va se terminer')
        elif event_type == 'customer.subscription.created':
            print(f'Abonnement créé : {event.id}')
        elif event_type == 'customer.subscription.updated':
            print(f'Abonnement mis à jour : {event.id}')
        elif event_type == 'customer.subscription.deleted':
            # Gérez l'annulation de l'abonnement ici.
            print(f'Abonnement annulé : {event.id}')

        # Répond avec un statut de succès
        return Response({'status': 'success'})
