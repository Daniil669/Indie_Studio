from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
import uuid
from forum.models import Thread  # Import Thread to list user's threads

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require verification to activate
            user.save()
            # Profile created via signal

            profile = user.profile
            token = uuid.uuid4().hex
            profile.verification_token = token
            profile.save()

            verify_url = request.build_absolute_uri(reverse('accounts:verify', kwargs={'token': token}))
            send_mail(
                'Verify Your Account',
                f'Please click the link to verify your account: {verify_url}',
                'no-reply@yourstudiogames.com',  # Change to your from email
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'A verification email has been sent. Please check your inbox.')
            return redirect('accounts:login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_page.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:home')  # Or your homepage name
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login_page.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')  # Or your homepage name

@login_required
def profile(request):
    threads = Thread.objects.filter(author=request.user).order_by('-created_at')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    notifications = request.user.notifications.order_by('-created_at')[:10]  # Last 10 notifications

    context = {
        'user': request.user,
        'threads': threads,
        'user_form': user_form,
        'profile_form': profile_form,
        'notifications': notifications,
    }
    return render(request, 'accounts/profile_page.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keeps user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

def verify(request, token):
    profile = get_object_or_404(Profile, verification_token=token)
    user = profile.user
    user.is_active = True
    profile.is_verified = True
    profile.verification_token = None
    profile.save()
    user.save()
    messages.success(request, 'Your account has been verified! You can now log in.')
    return redirect('accounts:login')