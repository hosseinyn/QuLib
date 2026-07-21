from user.models import Badge
from django.db.models import QuerySet
from django.contrib.auth.models import User

def get_user_badges(user: User) -> QuerySet[Badge]:
    """
    Retrieve all badges belonging to a specific user.

    Args:
        user (User): The user whose badges are to be retrieved.

    Returns:
        QuerySet[Badge]: A queryset of Badge objects.

    document by AI
    """
    return Badge.objects.filter(user=user).select_related('user')
