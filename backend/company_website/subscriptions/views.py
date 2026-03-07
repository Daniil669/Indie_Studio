from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .forms import SubscriptionForm
from .models import Subscriber
import uuid

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if not created and subscriber.confirmed:
                messages.info(request, 'You are already subscribed.')
                return redirect('core:home')  # Or wherever the form is

            # Generate token for double-opt-in
            token = uuid.uuid4().hex
            subscriber.confirmation_token = token
            subscriber.save()

            confirm_url = request.build_absolute_uri(reverse('subscriptions:confirm', kwargs={'token': token}))
            send_mail(
                'Confirm Your Subscription',
                f'Please click the link to confirm your subscription: {confirm_url}',
                'no-reply@yourstudiogames.com',  # Change to your from email
                [email],
                fail_silently=False,
            )
            messages.success(request, 'A confirmation email has been sent. Please check your inbox.')
            return redirect('core:home')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/subscribe.html', {'form': form})  # Optional standalone page; but since it's in footer, use POST directly

def confirm(request, token):
    try:
        subscriber = Subscriber.objects.get(confirmation_token=token)
        subscriber.confirmed = True
        subscriber.confirmation_token = None
        subscriber.save()
        messages.success(request, 'Your subscription has been confirmed!')
    except Subscriber.DoesNotExist:
        messages.error(request, 'Invalid confirmation link.')
    return redirect('core:home')