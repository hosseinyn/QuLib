from library.repositories.book_repository import (
    get_book_by_slug, get_book_by_id, 
    search_books_database , search_books_elasticsearch,
    get_filtered_books_by_params
)
from user.repositories.like_repository import check_like_exists, create_like, get_like
from user.repositories.comment_repository import get_comments_by_book, check_comments_by_book, get_comment_by_id, create_comment
from user.repositories.user_profile_repository import get_user_profile
from ai.utils import is_offensive
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from typing import Tuple, Dict, Any
from django.conf import settings
from user.repositories.user_profile_repository import update_user_score

def get_filtered_books(request_post_data):
    grades = []
    if request_post_data.get("hashtom"): grades.append("هشتم")
    if request_post_data.get("haftom"): grades.append("هفتم")
    if request_post_data.get("nohom"): grades.append("نهم")

    types = []
    if request_post_data.get("amoozeshi"): types.append("آموزشی")
    if request_post_data.get("emtahani"): types.append("امتحانی")
    if request_post_data.get("gambegam"): types.append("گام به گام")

    is_downloadable = bool(request_post_data.get("downloadble"))
    is_not_downloadable = bool(request_post_data.get("not-downloadble"))

    return get_filtered_books_by_params(grades, types, is_downloadable, is_not_downloadable)

def search_books(query: str):
    if settings.PRODUCTION:
        return search_books_elasticsearch(query)

    return search_books_database(query)

def get_edit_comment_data(user, slug, comment_id):
    data = get_book_page_data(user, slug)
    comment = get_comment_by_id(comment_id)
    data["comment_message"] = comment.message
    data["comment_id"] = comment_id
    return data

def process_edit_comment(user, slug, comment_id, message, rate):
    check_offensive = is_offensive(message)
    if not check_offensive:
        comment = get_comment_by_id(comment_id)
        if comment.comment_by != user:
            return False, get_book_page_data(user, slug)
        comment.message = message
        comment.score = rate
        comment.save()
        return True, get_book_page_data(user, slug)
    else:
        data = get_book_page_data(user, slug)
        data["error"] = "نظر شما منتشر نشد! قوانین رو بخون!"
        return False, data

def get_book_page_data(user, slug):
    book = get_book_by_slug(slug)
    if not book:
        return None
    
    is_liked = False
    if user.is_authenticated:
        is_liked = check_like_exists(user, book=book)

    check_comments = check_comments_by_book(book)
    
    if check_comments:
        comments = list(get_comments_by_book(book))
        comments_count = len(comments)
        total_score = sum(c.score for c in comments)
        average_comments_score = int(total_score / comments_count) if comments_count > 0 else 0
        average_comments_scores = range(1, average_comments_score + 1)
    else:
        average_comments_score = 0
        average_comments_scores = range(0)
        comments_count = 0
        comments = []

    return {
        "book": book,
        "is_liked": is_liked,
        "comments": comments,
        "comments_count": comments_count,
        "avg_scores": average_comments_scores,
        "avg_score": average_comments_score
    }

@transaction.atomic
def process_book_comment(user: User, slug: str, message: str, rate: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Process adding a new comment to a book.
    
    Args:
        user (User): The authenticated user making the comment.
        slug (str): The slug of the book.
        message (str): The comment message.
        rate (int): The rating given by the user.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: Success status and context data.
        
    document by AI
    """
    book = get_book_by_slug(slug)
    user_profile = get_user_profile(user)

    check_offensive = is_offensive(message)
    if not check_offensive:
        create_comment(
            comment_by=user,
            user_profile=user_profile,
            message=message,
            score=rate,
            book=book
        )
        update_user_score(user, user_profile)
        return True, get_book_page_data(user, slug)
    else:
        data = get_book_page_data(user, slug)
        data["error"] = "نظر شما منتشر نشد! قوانین رو بخون!"
        return False, data

def process_delete_comment(user, comment_id):
    comment = get_comment_by_id(comment_id)
    if comment.comment_by == user:
        comment.delete()

@transaction.atomic
def process_like_book(user: User, book_id: int) -> None:
    """
    Process liking a book by a user.
    
    Args:
        user (User): The authenticated user.
        book_id (int): The ID of the book to like.
        
    document by AI
    """
    book = get_book_by_id(book_id)
    if not check_like_exists(user, book=book):
        book.likes_count = F('likes_count') + 1
        book.save()
        create_like(user, book=book)
        update_user_score(user)

@transaction.atomic
def process_unlike_book(user: User, book_id: int) -> None:
    """
    Process unliking a book by a user.
    
    Args:
        user (User): The authenticated user.
        book_id (int): The ID of the book to unlike.
        
    document by AI
    """
    book = get_book_by_id(book_id)
    if check_like_exists(user, book=book):
        book.likes_count = F('likes_count') - 1
        book.save()
        last_like = get_like(user, book=book)
        last_like.delete()
        update_user_score(user)
