from django.contrib.auth import get_user_model
from support.utils.mail_sender import send_mail_to_support

User = get_user_model()

# def handle_subscription_created(event_data):
#     # enregistrer la souscription dans la base de données

def handle_subscription_activated(event_data):
    sub_id = event_data['resource']['id']
    user = User.objects.get(sub_id=sub_id)
    user.api_access = True
    user.save()

    subject = f"Subscription activated for {user.email}"
    content = f"Subscription activated for {user.email} : unique_id = {user.unique_id}, sub_id = {user.sub_id}, api_access = {user.api_access}."
    send_mail_to_support(subject, content)

# def handle_payment_completed(event_data):
#     # enregistrer le paiement réussi

# def handle_payment_failed(event_data):
#     # traiter le paiement échoué (suspension, contact utilisateur)

def handle_subscription_suspended(event_data):
    sub_id = event_data['resource']['id']
    user = User.objects.get(sub_id=sub_id)
    user.api_access = False
    user.save()

def handle_subscription_cancelled(event_data):
    sub_id = event_data['resource']['id']
    user = User.objects.get(sub_id=sub_id)
    user.api_access = False
    user.sub_id = None
    user.save()
    subject = f"Subscription cancelled for {user.email}"
    content = f"Subscription cancelled for {user.email} : unique_id = {user.unique_id}, sub_id = {user.sub_id}, api_access = {user.api_access}."
    send_mail_to_support(subject, content)
