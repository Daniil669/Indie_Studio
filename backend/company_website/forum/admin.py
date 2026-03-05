from django.contrib import admin
from .models import Thread, ForumPost

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at')