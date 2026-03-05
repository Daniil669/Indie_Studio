from django.urls import path
from . import views
from .views import ThreadListView, ThreadDetailView, create_thread, add_post

app_name = 'forum'

urlpatterns = [
    # path('forum/', views.forum, name='forum'),
    path('', ThreadListView.as_view(), name='list'),
    path('new/', create_thread, name='create_thread'),
    path('<slug:slug>/', ThreadDetailView.as_view(), name='detail'),
    path('<slug:slug>/post/', add_post, name='add_post'),
]