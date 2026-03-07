from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('confirm/<str:token>/', views.confirm, name='confirm'),
]