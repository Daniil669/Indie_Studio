from django.shortcuts import render
from games.models import Game  # Import Game model from games app
from blog.models import Post   # Import Post model from blog app
from tools.models import Tool  # Import Tool model from tools app

def home(request):
    # Fetch featured/latest data for homepage
    games = Game.objects.filter(featured=True)[:4]  # Assuming 'featured' field; or use .order_by('-released')[:4]
    posts = Post.objects.order_by('-created_at')[:3]  # Latest 3 blog posts
    tools = Tool.objects.filter(featured=True)[:3]  # Assuming 'featured' field; or .all()[:3]
    
    context = {
        'games': games,
        'posts': posts,
        'tools': tools,
    }
    return render(request, 'core/home_page.html', context)

def about(request):
    # About page is mostly static; add context if you have dynamic data like team members
    return render(request, 'core/about_page.html')