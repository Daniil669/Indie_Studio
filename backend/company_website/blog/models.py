from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User  # Assuming User for author
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from subscriptions.models import Subscriber

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

    def get_reaction_count(self, reaction_type):
        return self.reactions.filter(reaction_type=reaction_type).count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)  # Mods can approve if needed

    class Meta:
        permissions = [("can_comment", "Can add comments")]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'reaction_type')
        permissions = [("can_react", "Can add reactions")]

    def __str__(self):
        return f"{self.reaction_type} by {self.user} on {self.post}"
    

@receiver(post_save, sender=Post)  # Or for Game
def send_update_email(sender, instance, created, **kwargs):
    if created:
        subject = f'New Blog Post: {instance.title}'
        message = f'Check out our new post: {instance.get_absolute_url()}'
        from_email = 'no-reply@yourstudiogames.com'
        subscribers = Subscriber.objects.filter(confirmed=True).values_list('email', flat=True)
        emails = [(subject, message, from_email, [email]) for email in subscribers]
        send_mass_mail(emails, fail_silently=True)