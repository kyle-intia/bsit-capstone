from django.urls import path

from .views import (login_view, signup_view, verify_email, o_auth_login, verification_alert, verification_resend, logout_view,
                    pre_intro, pre_transpo, pre_food, pre_elec, pre_submit,
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

      # Pre-Assessment
    path('pre_intro/', pre_intro, name='pre_intro'),
    path('pre_transpo/', pre_transpo, name='pre_transpo'),
    path('pre_food/', pre_food, name='pre_food'),
    path('pre_elec/', pre_elec, name='pre_elec'),
    path('pre_submit/', pre_submit, name='pre_submit'),
]
