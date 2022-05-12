from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from time import sleep


@shared_task(max_retries=20)
def register_mail(email, otp):
    print("Done")
    sleep(1)  # sleeps for 1 seconds
    email_template = render_to_string('register.html',
                                      {"otp": otp})
    sign_up = EmailMultiAlternatives(
        "User OTP Verification",
        "User OTP Verification",
        settings.EMAIL_HOST_USER,
        [email],
    )
    sign_up.attach_alternative(email_template, 'text/html')
    sign_up.send()


@shared_task(max_retries=20)
def verify_mail(email):
    sleep(1)
    email_template = render_to_string('success.html')
    success = EmailMultiAlternatives(
        "Registration Successful",
        "Account activated Successfully",
        settings.EMAIL_HOST_USER,
        [email],
    )
    success.attach_alternative(email_template, 'text/html')
    success.send()


@shared_task(max_retries=20)
def forgot_mail(email, otp):
    sleep(1)
    email_template = render_to_string('forgot.html',
                                      {"otp": otp})
    forgot = EmailMultiAlternatives(
        "Forgot Password",
        "Forgot Password",
        settings.EMAIL_HOST_USER,
        [email],
    )
    forgot.attach_alternative(email_template, 'text/html')
    forgot.send()


@shared_task(max_retries=20)
def reset_mail(email):
    sleep(1)
    email_template = render_to_string('reset.html')
    reset = EmailMultiAlternatives(
        "Password Reset",
        "Password Reset",
        settings.EMAIL_HOST_USER,
        [email],
    )
    reset.attach_alternative(email_template, 'text/html')
    reset.send()


@shared_task(max_retries=20)
def subscribed_mail(email):
    sleep(1)
    email_template = render_to_string('subscibe.html',
                                      {
                                          "email": email
                                      })
    reset = EmailMultiAlternatives(
        "Greetings from e-learning",
        "Please check out our new course",
        settings.EMAIL_HOST_USER,
        [email],
    )
    reset.attach_alternative(email_template, 'text/html')
    reset.send()
