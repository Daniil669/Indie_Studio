from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User  # Assuming User for author

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    excerpt = models.TextField(max_length=300, blank=True)  # Short description for cards
    content = models.TextField()  # Full blog content
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt:
            self.excerpt = self.content[:300] + '...'  # Auto-generate if blank
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"