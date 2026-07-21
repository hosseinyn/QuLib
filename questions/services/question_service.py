from questions.repositories.question_repository import (
    get_question_by_slug, get_question_by_id, 
    search_questions_database , search_questions_elasticsearch,
    get_filtered_questions_by_params
)
from user.repositories.like_repository import check_like_exists, create_like, get_like
from user.repositories.comment_repository import get_comments_by_question, check_comments_by_question, get_comment_by_id, create_comment
from user.repositories.user_profile_repository import get_user_profile , update_user_score
from ai.utils import is_offensive
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from typing import Tuple, Dict, Any
from django.conf import settings

def get_filtered_questions(request_post_data):
    grades = []
    if request_post_data.get("hashtom"): grades.append("هشتم")
    if request_post_data.get("haftom"): grades.append("هفتم")
    if request_post_data.get("nohom"): grades.append("نهم")

    nobats = []
    if request_post_data.get("nobat1"): nobats.append("نوبت1")
    if request_post_data.get("nobat2"): nobats.append("نوبت2")

    times = []
    if request_post_data.get("mostamar"): times.append("مستمر")
    if request_post_data.get("payani"): times.append("پایانی")

    difficulties = []
    if request_post_data.get("hard"): difficulties.append("سخت")
    if request_post_data.get("medium"): difficulties.append("متوسط")
    if request_post_data.get("easy"): difficulties.append("راحت")

    return get_filtered_questions_by_params(grades, nobats, times, difficulties)

def search_questions(query: str):
    if settings.PRODUCTION:
        return search_questions_elasticsearch(query)

    return search_questions_database(query)

def get_question_page_data(user, slug):
    question = get_question_by_slug(slug)
    if not question:
        return None
    
    is_liked = False
    if user.is_authenticated:
        is_liked = check_like_exists(user, question=question)

    check_comments = check_comments_by_question(question)
    
    if check_comments:
        comments = list(get_comments_by_question(question))
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
        "question": question,
        "is_liked": is_liked,
        "comments": comments,
        "comments_count": comments_count,
        "avg_scores": average_comments_scores,
        "avg_score": average_comments_score
    }

@transaction.atomic
def process_question_comment(user: User, slug: str, message: str, rate: int) -> Tuple[bool, Dict[str, Any]]:
    """
    Process adding a new comment to a question.
    
    Args:
        user (User): The authenticated user making the comment.
        slug (str): The slug of the question.
        message (str): The comment message.
        rate (int): The rating given by the user.
        
    Returns:
        Tuple[bool, Dict[str, Any]]: Success status and context data.
        
    document by AI
    """
    question = get_question_by_slug(slug)
    user_profile = get_user_profile(user)

    check_offensive = is_offensive(message)
    if not check_offensive:
        create_comment(
            comment_by=user,
            user_profile=user_profile,
            message=message,
            score=rate,
            question=question
        )
        update_user_score(user, user_profile)
        return True, get_question_page_data(user, slug)
    else:
        data = get_question_page_data(user, slug)
        data["error"] = "نظر شما منتشر نشد! قوانین رو بخون!"
        return False, data

def get_edit_comment_data(user, slug, comment_id):
    data = get_question_page_data(user, slug)
    comment = get_comment_by_id(comment_id)
    data["comment_message"] = comment.message
    data["comment_id"] = comment_id
    return data

def process_edit_comment(user, slug, comment_id, message, rate):
    check_offensive = is_offensive(message)
    if not check_offensive:
        comment = get_comment_by_id(comment_id)
        if comment.comment_by != user:
            return False, get_question_page_data(user, slug)
        comment.message = message
        comment.score = rate
        comment.save()
        return True, get_question_page_data(user, slug)
    else:
        data = get_question_page_data(user, slug)
        data["error"] = "نظر شما منتشر نشد! قوانین رو بخون!"
        return False, data

def process_delete_comment(user, comment_id):
    comment = get_comment_by_id(comment_id)
    if comment.comment_by == user:
        comment.delete()

@transaction.atomic
def process_like_question(user: User, question_id: int) -> None:
    """
    Process liking a question by a user.
    
    Args:
        user (User): The authenticated user.
        question_id (int): The ID of the question to like.
        
    document by AI
    """
    question = get_question_by_id(question_id)
    if not check_like_exists(user, question=question):
        question.likes_count = F('likes_count') + 1
        question.save()
        create_like(user, question=question)
        update_user_score(user)

@transaction.atomic
def process_unlike_question(user: User, question_id: int) -> None:
    """
    Process unliking a question by a user.
    
    Args:
        user (User): The authenticated user.
        question_id (int): The ID of the question to unlike.
        
    document by AI
    """
    question = get_question_by_id(question_id)
    if check_like_exists(user, question=question):
        question.likes_count = F('likes_count') - 1
        question.save()
        last_like = get_like(user, question=question)
        last_like.delete()
        update_user_score(user)
