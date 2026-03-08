from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls')),  # Includes home and about from core
    path('games/', include('games.urls', namespace='games')),
    path('tools/', include('tools.urls', namespace='tools')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
