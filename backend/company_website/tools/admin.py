from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('featured',)