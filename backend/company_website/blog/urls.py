from django.urls import path
from . import views
from .views import PostListView, PostDetailView, add_comment, add_reaction

app_name = 'blog'

urlpatterns = [
    # path('blog/', views.blog, name='blog'),

    path('', PostListView.as_view(), name='list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug:slug>/comment/', add_comment, name='add_comment'),
    path('<slug:slug>/react/<str:reaction_type>/', add_reaction, name='add_reaction'),
]
