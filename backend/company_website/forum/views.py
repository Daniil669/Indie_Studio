from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Thread, ForumPost
from .forms import ThreadForm, PostForm

# def forum(request):
#     return HttpResponse("Forum page")


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/threads_page.html'
    context_object_name = 'threads'
    ordering = ['-updated_at']

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_page.html'
    slug_field = 'slug'

@login_required
def create_thread(request):
    if request.user.profile.is_verified:
        if request.method == 'POST':
            form = ThreadForm(request.POST)
            if form.is_valid():
                thread = form.save(commit=False)
                thread.author = request.user
                thread.save()
                return redirect(thread.get_absolute_url())
        else:
            form = ThreadForm()
        return render(request, 'forum/create_thread.html', {'form': form})
    return redirect('forum:list')

@login_required
def add_post(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if request.user.profile.is_verified:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.author = request.user
                post.save()
                return redirect(thread.get_absolute_url())
        else:
            form = PostForm()
        return render(request, 'forum/add_post.html', {'form': form, 'thread': thread})
    return redirect(thread.get_absolute_url())