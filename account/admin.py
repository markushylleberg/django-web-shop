from django.contrib import admin
from .models import PasswordResetRequest, UserProfile

# Register your models here.
admin.site.register(PasswordResetRequest)
admin.site.register(UserProfile)