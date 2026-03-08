from django.urls import path
from . import views
from .views import PostListView, PostDetailView, add_comment, toggle_reaction

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/comment/', add_comment, name='add_comment'),
    path('<slug:slug>/toggle-react/<str:reaction_type>/', toggle_reaction, name='toggle_reaction'),
]
