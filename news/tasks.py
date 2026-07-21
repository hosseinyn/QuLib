from django.core.mail import get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from celery import shared_task

from typing import List

@shared_task
def send_newsletter_email(subject: str, message: str, recipient_list: List[str] , uuid: int) -> None:
    """
    Send a newsletter email to a list of recipients.

    Args:
        subject (str): The email subject.
        message (str): The email body.
        recipient_list (List[str]): List of recipient email addresses.
        id (int) : The subscriber id.

    document by AI
    """
            
    domain = settings.DOMAIN
    leave_url = f"{domain}/news/api/leave/{uuid}"
    logo_url = f"{domain}/static/images/Logo-white.png"
            
    context = {
        'leave_url': leave_url,
        'logo_url': logo_url,
        'message' : message,
        'subject' : subject
    }
            
    html_message = render_to_string('emails/news_email.html', context)
            
    plain_message = strip_tags(html_message)
            
    with get_connection(
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
                
                subject = subject
                email_from = "news@qulib.ir"
                recipient_list = recipient_list
                
                email_obj = EmailMultiAlternatives(
                    subject=subject,
                    body=plain_message,
                    from_email=email_from,
                    to=recipient_list,
                    connection=connection
                )
                
                email_obj.attach_alternative(html_message, "text/html")
                
                email_obj.send()