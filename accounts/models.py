from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    password_reset_token = models.UUIDField(null=True, blank=True, unique=True)
    password_reset_token_expiry = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def generate_email_verification_token(self):
        token = str(uuid.uuid4())
        self.email_verification_token = token
        self.save()
        return token
    
    def set_reset_token(self, expiry_minutes=60):
        self.password_reset_token = uuid.uuid4()
        self.password_reset_token_expiry = timezone.now() + timedelta(minutes=expiry_minutes)
        self.save()
        return self.password_reset_token
    
    def clear_reset_token(self):
        self.password_reset_token = None
        self.password_reset_token_expiry = None
        self.save()