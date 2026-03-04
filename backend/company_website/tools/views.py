from django.shortcuts import render
from django.http import HttpResponse

def tools(request):
    return HttpResponse("Tools page")
