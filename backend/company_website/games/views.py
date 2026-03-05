from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Game

# def games(request):
#     return HttpResponse("Games Page")


class GameListView(ListView):
    model = Game
    template_name = 'games/games_page.html'
    context_object_name = 'games'
    ordering = ['-released']  # Or whatever ordering you prefer

class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_page.html'
    slug_field = 'slug'