from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Create a new superuser with email, unique_id, and provider interactively'

    def handle(self, *args, **kwargs):
        email = input('Enter email: ')
        unique_id = input('Enter unique ID: ')
        provider = input('Enter provider: ')
        password = input('Enter password: ')

        if not email:
            self.stdout.write(self.style.ERROR('Email is required'))
            return
        if not unique_id:
            self.stdout.write(self.style.ERROR('Unique ID is required'))
            return
        if not provider:
            self.stdout.write(self.style.ERROR('Provider is required'))
            return
        if not password:
            self.stdout.write(self.style.ERROR('Password is required'))
            return

        User = get_user_model()
        try:
            User.objects.create_superuser(email=email,
                                          unique_id=unique_id,
                                          provider=provider,
                                          password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser {email} created successfully!"))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
