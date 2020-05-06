from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        from . signals import create_user_profile