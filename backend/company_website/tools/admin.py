from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'cover', 'excerpt', 'description', 'featured')  # Custom form layout
    list_filter = ('featured',)