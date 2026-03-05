from django.urls import path
from . import views
from .views import GameListView, GameDetailView

app_name = 'games'

urlpatterns = [
    # path('games/', views.games, name='games'),
    path('', GameListView.as_view(), name='list'),
    path('<slug:slug>/', GameDetailView.as_view(), name='detail'),
]