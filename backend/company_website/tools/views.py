from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Tool

def tools(request):
    return HttpResponse("Tools page")


class ToolListView(ListView):
    model = Tool
    template_name = 'tools/tools_page.html'
    context_object_name = 'tools'
    ordering = ['-created_at']

class ToolDetailView(DetailView):
    model = Tool
    template_name = 'tools/tool_page.html'
    slug_field = 'slug'
