import re

from django.conf import settings
from django.shortcuts import redirect


# EXEPTION_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
LOGIN_REQUIRED_URLS = []
ADMIN_URLS = []

# if hasattr(settings, 'EXEPTION_URLS'):
#     EXEPTION_URLS += [re.compile(url) for url in settings.EXEPTION_URLS]

if hasattr(settings, 'LOGIN_REQUIRED_URLS'):
    LOGIN_REQUIRED_URLS += [re.compile(url) for url in settings.LOGIN_REQUIRED_URLS]

if hasattr(settings, 'ADMIN_URLS'):
    ADMIN_URLS += [re.compile(url) for url in settings.ADMIN_URLS]


class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-AUTH'] = 'AUTHENTICATION RAN'


        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if any(url.match(path) for url in LOGIN_REQUIRED_URLS) or any(url.match(path) for url in ADMIN_URLS):
                print('user is not logged in')
                return redirect(settings.LOGIN_URL)
        else:
            if not request.user.is_superuser:
                if any(url.match(path) for url in ADMIN_URLS):
                    print('user is not admin and trying to access admin pages')
                    return redirect(settings.SHOP_URL)

        # if not request.user.is_authenticated:
        #     if not any(url.match(path) for url in EXEPTION_URLS):
        #         print('user is not logged in')
        #         return redirect(settings.LOGIN_URL)
        # elif not request.user.is_superuser:
        #     if any(url.match(path) for url in ADMIN_URLS):
        #         print('user is not admin and trying to access admin pages')
        #         return redirect(settings.SHOP_URL)