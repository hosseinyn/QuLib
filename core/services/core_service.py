from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from user.repositories.user_profile_repository import get_top_users_by_score

def process_contact_form(cleaned_data):
    message_subject = cleaned_data["subject"]
    name = cleaned_data["name"]
    email = cleaned_data["email"]
    message_text = cleaned_data["message"]
    message_kind = cleaned_data["kind_of_message"]

    final_subject = f"{message_subject} | {message_kind}"
    final_message = f"{name} \n {message_text}"

    with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
            ) as connection:  
                subject = final_subject
                email_from = email
                recipient_list = [settings.EMAIL_HOST_USER, ]  
                message = final_message  
                EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
    
    return True

def get_leaderboard_users():
    return get_top_users_by_score(limit=10)
