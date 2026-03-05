from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Post, Comment, Reaction
from .forms import CommentForm

# def blog(request):
#     return HttpResponse("Blog page")


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
        choices = [choice[0] for choice in Reaction.REACTION_CHOICES]
        context['reaction_data'] = [
            {
                'type': choice,
                'title': choice.title(),
                'count': self.object.get_reaction_count(choice)
            }
            for choice in choices
        ]
        return context

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            if request.user.profile.is_verified:  # Assuming Profile model with is_verified
                comment.save()
                return redirect(post.get_absolute_url())
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

@login_required
def add_reaction(request, slug, reaction_type):
    post = get_object_or_404(Post, slug=slug)
    if request.user.profile.is_verified and reaction_type in dict(Reaction.REACTION_CHOICES).keys():
        Reaction.objects.get_or_create(post=post, user=request.user, reaction_type=reaction_type)
    return redirect(post.get_absolute_url())