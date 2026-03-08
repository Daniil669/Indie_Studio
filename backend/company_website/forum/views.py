# forum/views.py  # Updated for replies and notifications
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Thread, ForumPost, Notification
from .forms import ThreadForm, PostForm

class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/threads_page.html'
    context_object_name = 'threads'
    ordering = ['-updated_at']

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_page.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(parent=None)  # Top-level posts (for threading)
        return context

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
def add_post(request, slug, parent_id=None):
    thread = get_object_or_404(Thread, slug=slug)
    parent = get_object_or_404(ForumPost, id=parent_id) if parent_id else None
    if request.user.profile.is_verified:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.thread = thread
                post.author = request.user
                post.parent = parent
                post.save()
                # If reply, notify parent author
                if parent:
                    Notification.objects.create(
                        user=parent.author,
                        notification_type='reply',
                        message=f"{request.user.username} replied to your post.",
                        link=post.get_absolute_url()
                    )
                return redirect(thread.get_absolute_url())
        else:
            form = PostForm()
        return render(request, 'forum/add_post.html', {'form': form, 'thread': thread, 'parent': parent})
    return redirect(thread.get_absolute_url())