import django_rq
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as login_method, logout as logout_method
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from . messaging import new_password_req_email
from . models import PasswordResetRequest, UserProfile



def login(req):

    if req.user.is_authenticated: ### Check if user is already logged in
        return HttpResponseRedirect(reverse('shop:index'))

    context = {}
    if req.method == 'POST':
        username = req.POST['login-username']
        password = req.POST['login-password']

        user = authenticate(req, username=username, password=password)

        if user:
            login_method(req, user)
            return HttpResponseRedirect(reverse('shop:index'))
        else:
            context = {
                'message': 'Username or password are incorrect.'
            }
            
    return render(req, 'login.html', context)



def logout(req):

    logout_method(req)
    return HttpResponseRedirect(reverse('shop:index'))



def signup(req):

    context = {}
    if req.method == 'POST':
        if req.POST['first_name'] and req.POST['last_name'] and req.POST['username'] and req.POST['email'] and req.POST['password'] and req.POST['password_confirm']:
            firstname = req.POST['first_name']
            lastname = req.POST['last_name']
            username = req.POST['username']
            email = req.POST['email']
            password1 = req.POST['password']
            password2 = req.POST['password_confirm']

            try:
                validate_email(email)
            except ValidationError as error:
                print("Email is not valid:", error)
            else:
                if password1 == password2:
                    if len(password1) >= 8:
                        if User.objects.filter(username=username).exists(): ### Check if user already exists
                            context = {
                                'message': 'User already exists'
                            }
                        else:
                            User.objects.create_user(username, email, password1, first_name=firstname, last_name=lastname)
                            context = {
                                'message': 'User has been created! You can now go you the login page and login.'
                            }
                    else:
                        context = {
                            'message': 'Password must be a least 8 characters.'
                        }
                else:
                    context = {
                        'message': 'Passwords did not match.'
                    }
        else:
            context = {
                'message': 'Please fill out all fields.'
            }
        ### Input values
        # firstname = req.POST['first_name']
        # lastname = req.POST['last_name']
        # username = req.POST['username']
        # email = req.POST['email']
        # password1 = req.POST['password']
        # password2 = req.POST['password_confirm']


        # if password1 == password2: ### Check if passwords match
        #     if User.objects.filter(username=username).exists(): ### Check if user already exists
        #         context = {
        #             'message': 'User already exists'
        #         }
        #     else:
        #         User.objects.create_user(
        #             username, email, password1, first_name=firstname, last_name=lastname
        #         )
        #         context = {
        #             'message': 'User has been created! You can now go you the login page and login.'
        #         }
        # else:
        #     context = {
        #         'message': 'Passwords did not match.'
        #     }
    return render(req, 'signup.html', context)



def account_settings(req):

    user_details = UserProfile.objects.get(user=req.user.id)

    init_user_first_name = req.user.first_name
    init_user_last_name = req.user.last_name
    init_user_email = req.user.email

    init_userprofile_phone_number = user_details.phone_number
    init_userprofile_address = user_details.address
    init_userprofile_city = user_details.city
    init_userprofile_country = user_details.country

    context = {
        'first_name': req.user.first_name,
        'last_name': req.user.last_name,
        'email': req.user.email,
        'address': init_userprofile_address,
        'city': init_userprofile_city,
        'country': init_userprofile_country,
        'phone_number': init_userprofile_phone_number
    }

    if req.method == 'POST':
        first_name = req.POST['account_first_name']
        last_name = req.POST['account_last_name']
        email = req.POST['account_email']
        phone = req.POST['account_phone']
        address = req.POST['account_address']
        city = req.POST['account_city']
        country = req.POST['account_country']

        ## Check if any chances has been made to the User model
        if first_name is init_user_first_name and last_name is init_user_last_name and email is init_user_email:
            print('No changes in User model')
        else:
            user = User.objects.get(id=req.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            context = {
                'message': 'Your information has been updated!',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address,
                'city': city,
                'country': country,
                'phone_number': phone,
            }

        ## Check if any chances has been made to the User Profile model
        if phone is init_userprofile_phone_number and address is init_userprofile_address and city is init_userprofile_city and country is init_userprofile_country:
            print('No changes in UserProfile model')
        else:
            user_details.address = address
            user_details.city = city
            user_details.country = country
            user_details.phone_number = phone
            user_details.save()
            context = {
                'message': 'Your information has been updated!',
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address,
                'city': city,
                'country': country,
                'phone_number': phone,
            }

    return render(req, 'account_settings.html', context)


def request_reset_password(req):
    context = {}
    if req.method == 'POST':
        email = req.POST['reset-email']
        is_email_valid = User.objects.filter(email=email).exists()

        if is_email_valid: ### Check if email exists in our system
            new_request = PasswordResetRequest()
            new_request.email = email
            new_request.save()
            django_rq.enqueue(new_password_req_email, {
                'token': new_request.token,
                'email': new_request.email,
            })
            return HttpResponseRedirect(reverse('password_reset'))

        else:
            context = {
                'message': 'The email does not exists in our system'
            }

    return render(req, 'request_reset_password.html', context)

def password_reset(req):
    context = {}

    if req.method == 'POST':
        token = req.POST['pass-reset-token']
        email = req.POST['pass-reset-email']
        password = req.POST['pass-reset-password']
        password_confirm = req.POST['pass-reset-password-confirm']

        if password == password_confirm: ### Check if passwords match
            valid_token = PasswordResetRequest.objects.filter(token=token, active=True).exists()
            valid_user = User.objects.filter(email=email).exists()

            if valid_token and valid_user: ### Check if token exists and is active
                db_token = PasswordResetRequest.objects.get(token=token)
                db_token.active = False
                db_token.save()

                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()

                context = {
                    'success_message': f'Your password has succesfully been changed! Go back to the login page',
                    'message': False
                }
            else:
                context = {
                    'message': 'Invalid token or email.'
                }
        else:
            context = {
                'message': 'Passwords do not match.'
            }

    return render(req, 'password_reset.html', context)

def change_password(req):
    context = {}

    if req.method == 'POST':
        username = req.user.get_username()
        current_password = req.POST['change-current-password']
        new_password = req.POST['change-new-password']
        new_password_confirm = req.POST['change-new-password-confirm']

        if new_password == new_password_confirm: ### Check if new passwords match
            valid_user = authenticate(req, username=username, password=current_password)
            if valid_user: ### Check if current password is correct
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                context = {
                    'message': 'Your password has been updated!'
                }
            else:
                context = {
                    'message': 'Current password is wrong.'
                }
        else:
            context = {
                'message': 'Your new password do not match.'
            }

    return render(req, 'change_password.html', context)

def delete_account(req):
    context = {}
    if req.method == 'POST':
        username = req.user.get_username()
        password = req.POST['delete-password']
        text_delete = req.POST['delete-confirm']
        valid_user = authenticate(req, username=username, password=password)
        if valid_user: ### Check if password is correct
            if text_delete == 'delete':
                logout_method(req)
                user = User.objects.get(username=username)
                user.delete()
                return HttpResponseRedirect(reverse('login'))
            else:
                context = {
                    'message': '\'delete\' was not typed correctly.'
                }
        else:
            context = {
                'message': 'Wrong password.'
            }

    return render(req, 'delete_account.html', context)
    