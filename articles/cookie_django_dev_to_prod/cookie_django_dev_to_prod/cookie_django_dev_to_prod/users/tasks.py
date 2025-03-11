from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_welcome_email(email):
    to = email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'Welcome to Our Platform'
    html_message = render_to_string('users/new_user_welcome_email.html', {'email': to })
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
