from user.models import ForgotPassword

from user.models import ForgotPassword
from django.contrib.auth.models import User

def create_forgot_password_record(user: User, token: str) -> ForgotPassword:
    """
    Create a forgot password recovery record.

    Args:
        user (User): The user requesting password recovery.
        token (str): The secure token generated for recovery.

    Returns:
        ForgotPassword: The created recovery record.

    document by AI
    """
    return ForgotPassword.objects.create(
        user=user,
        token=token
    )

def get_forgot_password_record(token: str) -> ForgotPassword:
    """
    Retrieve a forgot password record by its token.

    Args:
        token (str): The recovery token.

    Returns:
        ForgotPassword: The matching recovery record.

    document by AI
    """
    return ForgotPassword.objects.get(token=token)

def delete_forgot_password_record(record: ForgotPassword) -> None:
    """
    Delete a forgot password recovery record.

    Args:
        record (ForgotPassword): The recovery record to delete.

    document by AI
    """
    record.delete()
