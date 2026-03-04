from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('tools/', views.tools, name='tools'),
]