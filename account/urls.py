from django.urls import path
from . import views

# app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('account_settings', views.account_settings, name='account_settings'),
    path('request_reset_password/', views.request_reset_password, name='request_reset_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password', views.change_password, name='change_password'),
    path('logout/', views.logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
]