from random import randint
from uuid import uuid4
from django.core.mail import get_connection
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from user.repositories.user_repository import get_user_by_email
from user.repositories.forgot_password_repository import create_forgot_password_record
from celery import shared_task

@shared_task
def send_welcome_email(username : str , email: str):
    domain = settings.DOMAIN
    logo_url = f"{domain}/static/images/Logo-white.png"
            
    context = {
        'logo_url': logo_url,
        'username' : username,
    }
            
    html_message = render_to_string('emails/welcome_email.html', context)
            
    plain_message = strip_tags(html_message)
            
    with get_connection(
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
                subject = "به کولیب خوش اومدی!"
                email_from = "help@qulib.ir"
                recipient_list = [email]
                
                email_obj = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=email_from,
                    to=recipient_list,
                    connection=connection
                )
                
                email_obj.attach_alternative(html_message, "text/html")
                
                email_obj.send()

@shared_task
def send_forgot_password_email(email : str):
        token = uuid4().hex
        user = get_user_by_email(email)
        create_forgot_password_record(user, token)
                
        domain = settings.DOMAIN
        recovery_url = f"{domain}/user/recovery-password/{token}"
        logo_url = f"{domain}/static/images/Logo-white.png"
                
        context = {
            'recovery_url': recovery_url,
            'logo_url': logo_url,
            'username' : user.username,
        }
                
        html_message = render_to_string('emails/password_recovery.html', context)
                
        plain_message = strip_tags(html_message)
                
        with get_connection(
                    host=settings.EMAIL_HOST, 
                    port=settings.EMAIL_PORT,  
                    username=settings.EMAIL_HOST_USER, 
                    password=settings.EMAIL_HOST_PASSWORD, 
                    use_tls=settings.EMAIL_USE_TLS  
                ) as connection:  
                    
                    subject = "فراموشی رمز عبور | کولیب"
                    email_from = "help@qulib.ir"
                    recipient_list = [email]
                    
                    email_obj = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=email_from,
                        to=recipient_list,
                        connection=connection
                    )
                    
                    email_obj.attach_alternative(html_message, "text/html")
                    
                    email_obj.send()