from django.contrib import admin
from .models import Post, Comment, Reaction

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'reaction_type')