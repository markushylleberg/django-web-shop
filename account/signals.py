from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, **kwargs):
    if not UserProfile.objects.filter(user=instance).exists():
        user_profile = UserProfile()
        user_profile.user = instance
        user_profile.save()