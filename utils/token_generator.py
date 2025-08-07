import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mass_mail, send_mail
from django.template.loader import render_to_string
from .common import get_name_from_email
from django.urls import reverse

def create_verification_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(days=1),  # Set expiration time
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def send_token(email):
    """
        sends email token
    """
    token = create_verification_token(email)
    name = get_name_from_email(email)

    subject = "Email confirmation link"
    message = (
        f"Hi {name},\n"
        f"Thanks for signing up. Follow the link to confirm your email:\n"
        f"{settings.DOMAIN}/email/verify/?token={token}\n\n"
        f"Regards,\nBrowseDocs Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,  
        recipient_list=[email]
    )
    return token


def create_password_reset_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(minutes=30),  # expires in 30 minutes
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def send_reset_token(user, request=None):
    token = create_password_reset_token(user.email)
    name = get_name_from_email(user.email)

    domain = request.get_host() if request else settings.DOMAIN
    scheme = request.scheme if request else "http"
    reset_url = f"{scheme}://{domain}{reverse('reset-password')}?token={token}"

    subject = "Reset your password"
    message = render_to_string('reset_password_email.html', {
        'email': user.email,
        'reset_url': reset_url,
        'name': name,
    })

    send_mail(
        subject=subject,
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=message,
    )


