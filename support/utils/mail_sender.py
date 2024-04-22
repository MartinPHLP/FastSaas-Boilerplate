from email.message import EmailMessage
import certifi
import smtplib
import ssl
import os

def send_mail_to_customer(subject, mail_path, destination):
    email_sender = os.getenv("SUPPORT_EMAIL")
    email_password = os.getenv("SUPPORT_EMAIL_PASSWORD")

    with open(mail_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = destination
    em['Subject'] = subject
    em.add_alternative(html_content, subtype='html')

    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(email_sender, email_password)
            server.send_message(em)
    except Exception as e:
        print(f"Une erreur est survenue lors de l'envoi de l'email : {str(e)}")

    print(f"Email envoyé à {destination}.")

def send_mail_to_support(subject, content, destination=None):
    email_sender = os.getenv("SUPPORT_EMAIL")
    email_password = os.getenv("SUPPORT_EMAIL_PASSWORD")

    if not destination:
        destination = email_sender

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = destination
    em['Subject'] = subject
    em.set_content(content)

    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(email_sender, email_password)
            server.send_message(em)
    except Exception as e:
        print(f"Une erreur est survenue lors de l'envoi de l'email : {str(e)}")

    print(f"Email envoyé à {destination}.")
