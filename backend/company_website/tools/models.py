from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Tool(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover = models.ImageField(upload_to='tools/covers/', blank=True, null=True)  # For card
    excerpt = models.TextField(max_length=300, blank=True)  # Short desc for card (new)
    description = RichTextField()  # Rich text for full page (headlines, paras, screenshots/videos/links)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt:
            self.excerpt = self.description[:300] + '...'  # Auto from rich desc
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/tools/{self.slug}/"