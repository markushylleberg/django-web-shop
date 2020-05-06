from django.db import models
from django.contrib.auth.models import User
from secrets import token_urlsafe

class PasswordResetRequest(models.Model):
    email = models.CharField(max_length=100)
    token = models.CharField(max_length=43, default=token_urlsafe)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Active: {self.active} // {self.token}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=90, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - User profile'