from django.contrib import admin
from .models import Thread, ForumPost, Notification

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')
    fields = ('thread', 'author', 'body', 'parent')  # Rich editor auto-applies

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'created_at', 'is_read')