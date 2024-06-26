from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, unique_id, provider, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, unique_id=unique_id, provider=provider, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, unique_id, provider, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('api_access', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, unique_id, provider, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Assurez-vous que le champ email est unique
    unique_id = models.CharField(max_length=255, unique=True)
    sub_id = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    provider = models.CharField(max_length=10)
    api_access = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['unique_id', 'provider']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
