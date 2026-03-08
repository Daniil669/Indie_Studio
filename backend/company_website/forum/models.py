from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Import for rich text (install django-ckeditor if not already)

class Thread(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/forum/{self.slug}/"

class ForumPost(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    body = RichTextField()  # Rich text for comments (text + images/videos via CKEditor)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # For threaded replies
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author} in {self.thread}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Handle mentions after save (parse body for @username)
        self.handle_mentions()

    def handle_mentions(self):
        # Simple parser for @username (improve with regex if needed)
        words = self.body.split()
        for word in words:
            if word.startswith('@'):
                username = word[1:].strip('.,!?')  # Strip punctuation
                try:
                    user = User.objects.get(username=username)
                    Notification.objects.create(
                        user=user,
                        notification_type='mention',
                        message=f"{self.author.username} mentioned you in a post.",
                        link=self.get_absolute_url()
                    )
                except User.DoesNotExist:
                    pass  # Invalid username, skip

    def get_absolute_url(self):
        return f"{self.thread.get_absolute_url()}#post-{self.id}"  # Anchor to post

# Notification model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('mention', 'Mention'),
        ('reply', 'Reply'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    link = models.URLField()  # Link to the post/reply
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"