from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'confirmed')
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        # Example: Send a simple email to selected subscribers
        for subscriber in queryset.filter(confirmed=True):
            send_mail(
                'New Update from Indie Studio',
                'Check out our latest blog post or game update! Visit: https://yourstudiogames.com',
                'no-reply@yourstudiogames.com',
                [subscriber.email],
                fail_silently=True,
            )
        self.message_user(request, f'Newsletter sent to {queryset.count()} subscribers.')