from django.conf import settings 
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django_ratelimit.exceptions import Ratelimited



def rate_limiter_view(request, *args, **kwargs):
    return render(request, 'ratelimit.html', status=429)


def view_404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler_403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return HttpResponse('Sorry too many requests, please wait', status=429)
    return HttpResponseForbidden('Forbidden')


def home_view(request):
    return render(request, 'home.html', status=200)


import jwt
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from user.models import User
from user.forms import CustomUserCreationForm
from utils.token_generator import send_token
from utils.token_generator import send_reset_token


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if User.objects.filter(email=email, is_active=False).exists():
            url = reverse('verification-alert') + f'?email={email}'
            return redirect(url)

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_token(user.email)
            return redirect(f"{reverse('verification-alert')}?email={user.email}")
        errors = [str(error[0]) for error in form.errors.values()]
        return render(request, 'signup.html', {'errors': errors})
    return render(request, 'signup.html')


def verify_email(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
        user = get_user_model().objects.get(email=email)
        user.is_active = True
        user.save()
        messages.success(request, "Account verified. You may now log in.")
        return redirect('login')
    except jwt.ExpiredSignatureError:
        return render(request, 'email-verification.html', {'error': 'Token expired. Request a new one.'})
    except Exception:
        return render(request, 'email-verification.html', {'error': 'Invalid token. Try again.'})


@require_http_methods(["GET", "POST"])
def verification_resend(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, 'resend-confirmation.html', {'error': f'{email} is not registered'})
        if user.is_active:
            return render(request, 'resend-confirmation.html', {'error': f'{email} is already verified'})

        send_token(email)
        return redirect(f"{reverse('verification-alert')}?email={email}")

    return render(request, 'resend-confirmation.html')


def verification_alert(request):
    email = request.GET.get('email') or ''
    return render(request, 'verification-alert.html', {
        'from_email': settings.EMAIL_HOST_USER,
        'to_email': email
    })


@require_http_methods(["GET", "POST"])
def forgot_password_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            send_reset_token(user, request)
            return render(request, 'forgot-password.html', {'message': 'Check your email for the reset link.'})
        else:
            return render(request, 'forgot-password.html', {'error': 'Email not found.'})

    return render(request, 'forgot-password.html')

@require_http_methods(["GET", "POST"])
def reset_password_form(request):
    token = request.GET.get('token')

    if not token:
        return render(request, 'reset_password.html', {'error': 'Missing token.'})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'reset_password.html', {'error': 'Invalid token user.'})
    except jwt.ExpiredSignatureError:
        return render(request, 'reset_password.html', {'error': 'Token expired. Request a new password reset.'})
    except Exception:
        return render(request, 'reset_password.html', {'error': 'Invalid token. Please try again.'})

    if request.method == "POST":
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successful. You may now log in.")
            return redirect('login')
        else:
            return render(request, 'reset_password.html', {'error': 'Please enter a new password.'})

    return render(request, 'reset_password.html')