from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Post, Comment, Reaction
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/posts_page.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_page.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emoji_map = {
            'like': '👍',
            'love': '❤️',
            'haha': '😂',
            'wow': '😲',
            'sad': '😢',
            'angry': '😡',
        }
        choices = [choice[0] for choice in Reaction.REACTION_CHOICES]
        user_reactions = set()
        if self.request.user.is_authenticated:
            user_reactions = set(Reaction.objects.filter(post=self.object, user=self.request.user).values_list('reaction_type', flat=True))
        context['reaction_data'] = [
            {
                'type': choice,
                'emoji': emoji_map.get(choice, choice.title()),
                'count': self.object.get_reaction_count(choice),
                'has_reacted': choice in user_reactions
            }
            for choice in choices
        ]
        return context

@login_required
def add_comment(request, slug):
    # Keep as before
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if request.user.profile.is_verified:
                comment.save()
                return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

@login_required
def toggle_reaction(request, slug, reaction_type):
    post = get_object_or_404(Post, slug=slug)
    if request.user.profile.is_verified and reaction_type in dict(Reaction.REACTION_CHOICES).keys():
        reaction, created = Reaction.objects.get_or_create(post=post, user=request.user, reaction_type=reaction_type)
        if not created:
            reaction.delete()  # Toggle: remove if exists
    return redirect(post.get_absolute_url())