from questions.models import Question
from django.db.models import Q
from user.repositories.user_profile_repository import get_user_profile
from user.repositories.like_repository import get_user_likes

from questions.models import Question
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from user.repositories.user_profile_repository import get_user_profile
from user.repositories.like_repository import get_user_likes
from typing import Optional, List
from questions.documents import QuestionDocument
from django.conf import settings

def get_all_questions() -> QuerySet[Question]:
    """
    Retrieve all questions.

    Returns:
        QuerySet[Question]: A queryset containing all Question objects.

    document by AI
    """
    return Question.objects.all()

def get_questions_for_list(user: Optional[User] = None) -> QuerySet[Question]:
    """
    Get a queryset of questions optimized for display.

    If a logged-in user is provided, retrieves recommendations based on the 
    user's grade, school, and likeness similarity to past liked questions.
    Otherwise, returns all questions ordered by likes.

    Args:
        user (Optional[User]): The authenticated user.

    Returns:
        QuerySet[Question]: The matching Question queryset.

    document by AI
    """

    if not (user and user.is_authenticated):
        if not settings.PRODUCTION:
            return (
                Question.objects.only(
                    "title",
                    "description",
                    "school_name",
                    "difficulty",
                    "slug",
                    "file",
                )
                .order_by("-likes_count")
            )

        return (
            QuestionDocument.search()
            .sort("-likes_count")
            .to_queryset()
        )

    user_profile = get_user_profile(user=user)
    user_likes = get_user_likes(user=user)

    if (
        not user_profile.grade
        or not user_profile.school_name
        or not user_likes.filter(book=None).exists()
    ):
        if not settings.PRODUCTION:
            return (
                Question.objects.only(
                    "title",
                    "description",
                    "school_name",
                    "difficulty",
                    "slug",
                    "file",
                )
                .order_by("-likes_count")
            )

        return (
            QuestionDocument.search()
            .sort("-likes_count")
            .to_queryset()
        )

    recent_likes = (
        user_likes.filter(book=None)
        .select_related("question")
        .order_by("-id")[:20]
    )

    liked_ids = [like.question_id for like in recent_likes]

    liked_schools = set()
    liked_difficulties = set()
    liked_writers = set()

    for like in recent_likes:
        if like.question:
            liked_schools.add(like.question.school_name)
            liked_difficulties.add(like.question.difficulty)
            liked_writers.add(like.question.writer)

    if not settings.PRODUCTION:
        similarity_q = Q()

        if liked_schools:
            similarity_q |= Q(school_name__in=liked_schools)

        if liked_difficulties:
            similarity_q |= Q(difficulty__in=liked_difficulties)

        if liked_writers:
            similarity_q |= Q(writer__in=liked_writers)

        return (
            Question.objects.filter(
                Q(grade=user_profile.grade)
                | Q(school_name=user_profile.school_name),
                similarity_q,
            )
            .exclude(id__in=liked_ids)
            .only(
                "title",
                "description",
                "school_name",
                "difficulty",
                "slug",
                "file",
            )
            .order_by("-likes_count")
        )

    should = []

    if liked_schools:
        should.append({"terms": {"school_name": list(liked_schools)}})

    if liked_difficulties:
        should.append({"terms": {"difficulty": list(liked_difficulties)}})

    if liked_writers:
        should.append({"terms": {"writer": list(liked_writers)}})

    search = (
        QuestionDocument.search()
        .query(
            "bool",
            filter=[
                {
                    "bool": {
                        "should": [
                            {"term": {"grade": user_profile.grade}},
                            {"term": {"school_name": user_profile.school_name}},
                        ],
                        "minimum_should_match": 1,
                    }
                }
            ],
            should=should,
            minimum_should_match=1 if should else 0,
            must_not=[
                {
                    "terms": {
                        "_id": [str(i) for i in liked_ids]
                    }
                }
            ],
        )
        .sort("-likes_count")
    )

    return search.to_queryset()

def get_filtered_questions_by_params(
    grades: List[str],
    nobats: List[str],
    times: List[str],
    difficulties: List[str],
) -> QuerySet[Question]:
    """
    Retrieve questions filtered by various criteria.

    Args:
        grades (List[str]): List of grades.
        nobats (List[str]): List of exam periods/tags.
        times (List[str]): List of exam types.
        difficulties (List[str]): List of difficulty levels.

    Returns:
        QuerySet[Question]: The filtered Question queryset.

    document by AI
    """

    if not settings.PRODUCTION:
        qs = get_questions_for_list()

        if grades:
            grade_q = Q()
            for grade in grades:
                grade_q |= Q(grade=grade)
            qs = qs.filter(grade_q)

        if nobats:
            nobat_q = Q()
            for nobat in nobats:
                nobat_q |= Q(tags__icontains=nobat)
            qs = qs.filter(nobat_q)

        if times:
            time_q = Q()
            for time in times:
                time_q |= Q(tags__icontains=time)
            qs = qs.filter(time_q)

        if difficulties:
            diff_q = Q()
            for diff in difficulties:
                diff_q |= Q(difficulty=diff)
            qs = qs.filter(diff_q)

        return qs

    search = QuestionDocument.search()

    if grades:
        search = search.filter("terms", grade=grades)

    if difficulties:
        search = search.filter("terms", difficulty=difficulties)

    if nobats:
        for nobat in nobats:
            search = search.filter(
                "match",
                tags=nobat,
            )

    if times:
        for time in times:
            search = search.filter(
                "match",
                tags=time,
            )

    return search.to_queryset()

def get_question_by_slug(slug: str) -> Question:
    """
    Retrieve a question by its slug.

    Args:
        slug (str): The unique slug of the question.

    Returns:
        Question: The matching Question instance.

    document by AI
    """
    try:
        return Question.objects.get(slug=slug)
    except:
        return None

def get_question_by_id(question_id: int) -> Question:
    """
    Retrieve a question by its database ID.

    Args:
        question_id (int): The database ID.

    Returns:
        Question: The matching Question instance.

    document by AI
    """
    return Question.objects.get(id=question_id)

def search_questions_database(query: str):
    """
        Search questions by default django ORM.
    
        Args:
            query (str): The search query.
    
        Returns:
            QuerySet[Question]: The matching Question queryset.
    
        document by AI
    """
    return Question.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(writer__icontains=query) |
        Q(tags__icontains=query) |
        Q(school_name__icontains=query)
    )

def search_questions_elasticsearch(query: str):
    """
        Search questions by Elasticsearch.
        
        Args:
            query (str): The search query.
        
        Returns:
            QuerySet[Question]: The matching Question queryset.
        
        document by AI
    """
    search = (
        QuestionDocument.search()
        .query(
            "multi_match",
            query=query,
            fields=[
                "title",
                "description",
                "writer",
                "tags",
                "school_name",
            ],
            fuzziness="AUTO",
        )
    )

    return search.to_queryset()
