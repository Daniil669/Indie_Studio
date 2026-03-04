from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('forum/', views.forum, name='forum'),
]