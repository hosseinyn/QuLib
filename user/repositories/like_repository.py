from user.models import Like

from user.models import Like
from django.contrib.auth.models import User
from questions.models import Question
from library.models import Book
from django.db.models import QuerySet
from typing import Optional, List

def get_user_likes(user: User) -> QuerySet[Like]:
    """
    Retrieve all like records belonging to a user.

    Args:
        user (User): The user whose likes to retrieve.

    Returns:
        QuerySet[Like]: A queryset of Like records.

    document by AI
    """
    return Like.objects.filter(liked_by=user)

def check_like_exists(user: User, question: Optional[Question] = None, book: Optional[Book] = None) -> bool:
    """
    Check if a user has liked a specific question or book.

    Args:
        user (User): The user to check.
        question (Optional[Question]): The question to check.
        book (Optional[Book]): The book to check.

    Returns:
        bool: True if a like exists, False otherwise.

    document by AI
    """
    if question:
        return Like.objects.filter(liked_by=user, question=question).exists()
    elif book:
        return Like.objects.filter(liked_by=user, book=book).exists()
    return False

def create_like(user: User, question: Optional[Question] = None, book: Optional[Book] = None) -> Like:
    """
    Create a new like record for a user on a question or book.

    Args:
        user (User): The user who likes the item.
        question (Optional[Question]): The question being liked.
        book (Optional[Book]): The book being liked.

    Returns:
        Like: The created Like record.

    document by AI
    """
    return Like.objects.create(liked_by=user, question=question, book=book)

def get_like(user: User, question: Optional[Question] = None, book: Optional[Book] = None) -> Like:
    """
    Retrieve a specific like record.

    Args:
        user (User): The user who liked the item.
        question (Optional[Question]): The liked question.
        book (Optional[Book]): The liked book.

    Returns:
        Like: The matching Like record.

    document by AI
    """
    if question:
        return Like.objects.get(liked_by=user, question=question)
    elif book:
        return Like.objects.get(liked_by=user, book=book)


def get_user_likes_count(user: User) -> int:
    """
    Get the total number of items liked by a user.

    Args:
        user (User): The user whose like count to retrieve.

    Returns:
        int: The number of likes.

    document by AI
    """
    return get_user_likes(user).count()

def get_liked_questions_for_user(user: User) -> List[Question]:
    """
    Get list of all questions liked by a user.

    Args:
        user (User): The user.

    Returns:
        List[Question]: A list of liked Question objects.

    document by AI
    """
    likes = get_user_likes(user).select_related('question')
    return [like.question for like in likes if like.question]

def get_liked_books_for_user(user: User) -> List[Book]:
    """
    Get list of all books liked by a user.

    Args:
        user (User): The user.

    Returns:
        List[Book]: A list of liked Book objects.

    document by AI
    """
    likes = get_user_likes(user).select_related('book')
    return [like.book for like in likes if like.book]
