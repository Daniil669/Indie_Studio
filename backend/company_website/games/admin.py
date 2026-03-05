from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'released', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('featured', 'released')