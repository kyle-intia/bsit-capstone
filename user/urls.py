from django.urls import path

from .views import (login_view, signup_view, verify_email, o_auth_login,
                    verification_alert, verification_resend, logout_view,
                    )


urlpatterns = [

    path('email/verify/', verify_email, name='verify-email'),

    path('email/verification/resend/', verification_resend, name='resend-verification'),
    path('email/verification-alert/', verification_alert, name='verification-alert'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('verify-email/', verify_email, name='verify-email'),
    path('verification-alert/', verification_alert, name='verification-alert'),
    path('resend-confirmation/', verification_resend, name='resend-confirmation'),
    path('forgot-password/', o_auth_login, name='forgot-password'),
]
