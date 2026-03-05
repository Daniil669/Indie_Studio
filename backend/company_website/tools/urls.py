from django.urls import path
from . import views
from .views import ToolListView, ToolDetailView

app_name = 'tools'

urlpatterns = [
    path('', ToolListView.as_view(), name='list'),
    path('<slug:slug>/', ToolDetailView.as_view(), name='detail'),

]