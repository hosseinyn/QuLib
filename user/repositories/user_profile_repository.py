from user.models import UserProfile

from user.models import UserProfile
from django.db.models import QuerySet
from django.contrib.auth.models import User
from typing import Optional
from .like_repository import get_user_likes_count
from .comment_repository import get_user_comments_count

def get_top_users_by_score(limit: int = 10) -> QuerySet[UserProfile]:
    """
    Retrieve user profiles with the highest scores.

    Args:
        limit (int): The maximum number of user profiles to return.

    Returns:
        QuerySet[UserProfile]: A queryset of top user profiles.

    document by AI
    """
    return UserProfile.objects.select_related('user').order_by('-score')[:limit]

def get_user_profile(user: User) -> UserProfile:
    """
    Retrieve the profile of a specific user.

    Args:
        user (User): The user whose profile is to be retrieved.

    Returns:
        UserProfile: The corresponding profile object.

    document by AI
    """
    return UserProfile.objects.select_related('user').get(user=user)

def get_user_grade(user: str) -> Optional[str]:
    """
    Retrieve the grade of a user by their username.

    Args:
        user (str): The username of the user.

    Returns:
        Optional[str]: The grade of the user, or None.

    document by AI
    """
    return UserProfile.objects.select_related('user').get(user__username=user).grade

def create_user_profile(user: User, grade: str, school_name: str) -> UserProfile:
    """
    Create a new user profile record.

    Args:
        user (User): The associated user.
        grade (str): The user's grade.
        school_name (str): The user's school name.

    Returns:
        UserProfile: The created user profile.

    document by AI
    """
    return UserProfile.objects.create(
        user=user,
        grade=grade,
        school_name=school_name
    )

def update_user_score(user, user_profile=None):
    if not user_profile:
        user_profile = get_user_profile(user)
    user_likes_count = get_user_likes_count(user)
    user_comments_count = get_user_comments_count(user)
    user_profile.score = (user_likes_count + user_comments_count) / 2
    user_profile.save()
