from django.contrib.auth.models import User

def check_user_exists_by_email(email: str) -> bool:
    """
    Check if a user exists with the given email address.

    Args:
        email (str): The email to check.

    Returns:
        bool: True if the user exists, False otherwise.

    document by AI
    """
    return User.objects.filter(email=email).exists()

def check_user_exists_by_username(username: str) -> bool:
    """
    Check if a user exists with the given username.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.

    document by AI
    """
    return User.objects.filter(username=username).exists()

def get_user_by_email(email: str) -> User:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email of the user.

    Returns:
        User: The matching User instance.

    document by AI
    """
    return User.objects.get(email=email)

def get_user_by_username(username: str) -> User:
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user.

    Returns:
        User: The matching User instance.

    document by AI
    """
    return User.objects.get(username=username)

def create_user(email: str, password: str, username: str) -> User:
    """
    Create and return a new User with email, password, and username.

    Args:
        email (str): The email address.
        password (str): The password.
        username (str): The username.

    Returns:
        User: The created User instance.

    document by AI
    """
    return User.objects.create_user(
        email=email,
        password=password,
        username=username
    )

def delete_user(username: str) -> None:
    """
    Delete a user by their username.

    Args:
        username (str): The username of the user to delete.

    document by AI
    """
    user = User.objects.get(username=username)
    user.delete()
