from django.shortcuts import render
from django.http import HttpResponse

def games(request):
    return HttpResponse("Games Page")
