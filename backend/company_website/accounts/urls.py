from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/profile', views.account, name='profile'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
    path('accounts/signup', views.signup, name='signup'),
]