from django.urls import path
from . import views

# app_name = 'account'

urlpatterns = [
    path('account_settings/', views.account_settings, name='account_settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('signup/', views.signup, name='signup'),
    path('request_reset_password/', views.request_reset_password, name='request_reset_password'),
]