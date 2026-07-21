from user.repositories.user_profile_repository import get_user_profile
from user.repositories.like_repository import get_user_likes_count, get_liked_questions_for_user, get_liked_books_for_user
from user.repositories.comment_repository import get_user_comments_count
from user.repositories.badge_repository import get_user_badges
from user.repositories.user_repository import check_user_exists_by_username, get_user_by_username, delete_user
from user.repositories.report_repository import create_delete_account_report

from django.db import transaction
from typing import Dict, Any, Tuple, Optional
from django.contrib.auth.models import User

def get_user_panel_data(user: User) -> Dict[str, Any]:
    """
    Retrieve data for the user's dashboard panel.
    
    Args:
        user (User): The authenticated user.
        
    Returns:
        Dict[str, Any]: A dictionary containing user stats and profile data.
        
    document by AI
    """
    user_data = get_user_profile(user)
    likes_count = get_user_likes_count(user)
    comments_count = get_user_comments_count(user)
    
    return {
        "likes_count": likes_count,
        "comments_count": comments_count,
        "score": user_data.score,
        "grade": user_data.grade,
        "school_name": user_data.school_name,
        "liked_questions": get_liked_questions_for_user(user),
        "liked_books": get_liked_books_for_user(user),
        "badges": get_user_badges(user),
        "profile_picture" : user_data.profile_picture
    }

def get_account_data(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve public account data for a specific username.
    
    Args:
        username (str): The username of the requested account.
        
    Returns:
        Optional[Dict[str, Any]]: The user's public data, or None if the user does not exist.
        
    document by AI
    """
    if not check_user_exists_by_username(username):
        return None
    user = get_user_by_username(username)
    data = get_user_panel_data(user)
    data["username"] = user.username
    return data

@transaction.atomic
def process_delete_account(username: str, reason: str) -> None:
    """
    Process account deletion and create a deletion report.
    
    Args:
        username (str): The username of the account to delete.
        reason (str): The user's provided reason for deletion.
        
    document by AI
    """
    create_delete_account_report(reason=reason)
    delete_user(username)

@transaction.atomic
def process_edit_profile(current_user: User, username: str, school_name: str, grade: str, profile_picture_id: int) -> Tuple[bool, str]:
    """
    Process updating the user's profile information.
    
    Args:
        current_user (User): The authenticated user making the request.
        username (str): The new username.
        school_name (str): The user's school name.
        grade (str): The user's grade.
        profile_picture_id (int): The ID of the selected profile picture.
        
    Returns:
        Tuple[bool, str]: A boolean indicating success, and a message.
        
    document by AI
    """
    user = get_user_by_username(current_user.username)
    user_profile = get_user_profile(user)
    
    check_username = check_user_exists_by_username(username)
    if not check_username or username == current_user.username:
        user.username = username
    else:
        return False, "این نام کاربری قبلا استفاده شده است"
    
    user_profile.school_name = school_name
    user_profile.grade = grade
    user_profile.profile_picture = profile_picture_id
    
    user.save()
    user_profile.save()
    return True, "Success"
