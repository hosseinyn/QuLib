from random import randint
from user.repositories.user_repository import check_user_exists_by_email, get_user_by_email, create_user, get_user_by_username
from user.repositories.forgot_password_repository import get_forgot_password_record, delete_forgot_password_record
from django.contrib.auth import authenticate, login as django_login
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.http import HttpRequest
from typing import Tuple, Optional
from user.models import ForgotPassword
from ..tasks import send_welcome_email , send_forgot_password_email

def process_login(request: HttpRequest, email: str, password: str) -> Tuple[bool, str]:
    """
    Process user login via email and password.
    
    Args:
        request (HttpRequest): The current HTTP request.
        email (str): The user's email address.
        password (str): The user's password.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and a message.
        
    document by AI
    """
    if check_user_exists_by_email(email):
        user = get_user_by_email(email)
        authenticated_user = authenticate(request, username=user.username, password=password)
        if authenticated_user is not None:
            django_login(request, authenticated_user)
            return True, "Success"
        return False, "ایمیل یا رمز عبور صحیح نیست"
    return False, "ایمیل یا رمز عبور صحیح نیست"

@transaction.atomic
def process_signup(email: str, password: str) -> Tuple[bool, str]:
    """
    Process user registration, creating a user and an initial profile.
    
    Args:
        email (str): The new user's email address.
        password (str): The new user's password.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and a message.
        
    document by AI
    """
    if check_user_exists_by_email(email):
        return False, "این آدرس ایمیل قبلا ثبت نام کرده!"
    
    random_username = 'student_' + str(randint(0,9999)).zfill(4)
    new_user = create_user(email, password, random_username)

    send_welcome_email.delay(random_username , email)
    return True, "Success"

def process_change_password(request: HttpRequest, old_password: str, new_password: str) -> Tuple[bool, str]:
    """
    Process password change for an authenticated user.
    
    Args:
        request (HttpRequest): The current HTTP request.
        old_password (str): The current password.
        new_password (str): The new password.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and a message.
        
    document by AI
    """
    check_password = authenticate(request, username=request.user.username, password=old_password)
    if check_password:
        user = get_user_by_username(request.user.username)
        user.set_password(new_password)
        user.save()
        return True, "Success"
    return False, "گذرواژه قبلی نادرست است."

def process_forgot_password(email: str) -> None:
    """
    Send a password recovery email to the user if the email exists.
    
    Args:
        email (str): The email address of the user.
        
    document by AI
    """
    if check_user_exists_by_email(email):
        # ساخت توکن برای لینک بازیابی رمز عبور
        send_forgot_password_email.delay(email)

def get_recovery_password_status(token: str) -> Tuple[bool, Optional[ForgotPassword]]:
    """
    Check if a password recovery token is valid and hasn't expired.
    
    Args:
        token (str): The recovery token.
        
    Returns:
        Tuple[bool, Optional[ForgotPassword]]: A boolean indicating validity, and the record if valid.
        
    document by AI
    """
    try:
        record = get_forgot_password_record(token)
    except:
        return False, None
    now = timezone.now()
    time_left = record.expire_date - now
    if time_left <= timedelta(hours=0):
        return False, None
    elif time_left <= timedelta(hours=4):
        return True, record
    return False, None

def process_recovery_password(request: HttpRequest, record: ForgotPassword, new_password: str) -> None:
    """
    Process password recovery and log the user in.
    
    Args:
        request (HttpRequest): The current HTTP request.
        record (ForgotPassword): The valid recovery record containing the user.
        new_password (str): The new password to set.
        
    document by AI
    """
    username = record.user.username
    user = get_user_by_username(username)
    user.set_password(new_password)
    user.save()
    delete_forgot_password_record(record)
    
    authenticated_user = authenticate(request, username=username, password=new_password)
    django_login(request, authenticated_user)
