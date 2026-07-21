from user.models import Comment

from user.models import Comment, UserProfile
from django.contrib.auth.models import User
from questions.models import Question
from library.models import Book
from django.db.models import QuerySet
from typing import Optional

def get_user_comments_count(user: User) -> int:
    """
    Get the total number of comments written by a specific user.

    Args:
        user (User): The user whose comment count to retrieve.

    Returns:
        int: The number of comments.

    document by AI
    """
    return Comment.objects.filter(comment_by=user).count()

def get_comments_by_question(question: Question) -> QuerySet[Comment]:
    """
    Get all comments for a specific question, optimized with select_related.

    Args:
        question (Question): The question instance.

    Returns:
        QuerySet[Comment]: A queryset of Comments.

    document by AI
    """
    return Comment.objects.filter(question=question).select_related('comment_by', 'user_profile')

def check_comments_by_question(question: Question) -> bool:
    """
    Check if any comments exist for a specific question.

    Args:
        question (Question): The question instance.

    Returns:
        bool: True if comments exist, False otherwise.

    document by AI
    """
    return Comment.objects.filter(question=question).exists()

def get_comments_by_book(book: Book) -> QuerySet[Comment]:
    """
    Get all comments for a specific book, optimized with select_related.

    Args:
        book (Book): The book instance.

    Returns:
        QuerySet[Comment]: A queryset of Comments.

    document by AI
    """
    return Comment.objects.filter(book=book).select_related('comment_by', 'user_profile')

def check_comments_by_book(book: Book) -> bool:
    """
    Check if any comments exist for a specific book.

    Args:
        book (Book): The book instance.

    Returns:
        bool: True if comments exist, False otherwise.

    document by AI
    """
    return Comment.objects.filter(book=book).exists()

def get_comment_by_id(comment_id: int) -> Comment:
    """
    Retrieve a specific comment by its ID.

    Args:
        comment_id (int): The database ID of the comment.

    Returns:
        Comment: The Comment instance.

    document by AI
    """
    return Comment.objects.get(id=comment_id)

def create_comment(
    comment_by: User,
    user_profile: UserProfile,
    message: str,
    score: int,
    question: Optional[Question] = None,
    book: Optional[Book] = None
) -> Comment:
    """
    Create a new comment on a question or a book.

    Args:
        comment_by (User): The author of the comment.
        user_profile (UserProfile): The profile of the author.
        message (str): The message content.
        score (int): The comment rating/score.
        question (Optional[Question]): The question the comment is on.
        book (Optional[Book]): The book the comment is on.

    Returns:
        Comment: The created Comment instance.

    document by AI
    """
    return Comment.objects.create(
        comment_by=comment_by,
        user_profile=user_profile,
        message=message,
        score=score,
        question=question,
        book=book
    )
