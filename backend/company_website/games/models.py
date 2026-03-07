from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from subscriptions.models import Subscriber

class Game(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover = models.ImageField(upload_to='games/covers/')
    preview_video = models.FileField(upload_to='games/previews/', blank=True, null=True)  # Optional video for hover
    description = models.TextField()
    released = models.DateField(blank=True, null=True)
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
        return f"/games/{self.slug}/"
    

@receiver(post_save, sender=Game)  # Or for Game
def send_update_email(sender, instance, created, **kwargs):
    if created:
        subject = f'New Blog Post: {instance.title}'
        message = f'Check out our new post: {instance.get_absolute_url()}'
        from_email = 'no-reply@yourstudiogames.com'
        subscribers = Subscriber.objects.filter(confirmed=True).values_list('email', flat=True)
        emails = [(subject, message, from_email, [email]) for email in subscribers]
        send_mass_mail(emails, fail_silently=True)