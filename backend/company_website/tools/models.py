# tools/models.py
from django.db import models
from django.utils.text import slugify

class Tool(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover = models.ImageField(upload_to='tools/covers/', blank=True, null=True)
    description = models.TextField()
    featured = models.BooleanField(default=False)  # For homepage teaser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/tools/{self.slug}/"