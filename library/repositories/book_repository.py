from library.models import Book
from django.db.models import Q
from user.repositories.user_profile_repository import get_user_profile
from user.repositories.like_repository import get_user_likes


from library.models import Book
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from user.repositories.user_profile_repository import get_user_profile
from user.repositories.like_repository import get_user_likes
from typing import Optional, List
from library.documents import BookDocument
from django.conf import settings


def get_all_books() -> QuerySet[Book]:
    """
    Retrieve all books.

    Returns:
        QuerySet[Book]: A queryset containing all Book objects.

    document by AI
    """
    return Book.objects.all()

def get_books_for_list(user: Optional[User] = None) -> QuerySet[Book]:
    """
    Get a queryset of books optimized for display.

    If a logged-in user is provided, retrieves recommendations based on the 
    user's grade, school, and likeness similarity to past liked books.
    Otherwise, returns all books ordered by likes.

    Args:
        user (Optional[User]): The authenticated user.

    Returns:
        QuerySet[Book]: The matching Book queryset.

    document by AI
    """

    if not (user and user.is_authenticated):
        if not settings.PRODUCTION:
            return Book.objects.only(
                "title",
                "description",
                "school_name",
                "publisher",
                "slug",
                "is_downloadable",
                "file",
            ).order_by("-likes_count")

        return (
            BookDocument.search()
            .sort("-likes_count")
            .to_queryset()
        )

    user_profile = get_user_profile(user=user)
    user_likes = get_user_likes(user=user)

    if (
        not user_profile.grade
        or not user_profile.school_name
        or not user_likes.filter(question=None).exists()
    ):
        if not settings.PRODUCTION:
            return Book.objects.only(
                "title",
                "description",
                "school_name",
                "publisher",
                "slug",
                "is_downloadable",
                "file",
            ).order_by("-likes_count")

        return (
            BookDocument.search()
            .sort("-likes_count")
            .to_queryset()
        )

    recent_likes = (
        user_likes.filter(question=None)
        .select_related("book")
        .order_by("-id")[:20]
    )

    liked_ids = [like.book_id for like in recent_likes]

    liked_schools = set()
    liked_publishers = set()
    liked_writers = set()

    for like in recent_likes:
        if like.book:
            liked_schools.add(like.book.school_name)
            liked_publishers.add(like.book.publisher)
            liked_writers.add(like.book.writer)

    if not settings.PRODUCTION:
        similarity_q = Q()

        if liked_schools:
            similarity_q |= Q(school_name__in=liked_schools)

        if liked_publishers:
            similarity_q |= Q(publisher__in=liked_publishers)

        if liked_writers:
            similarity_q |= Q(writer__in=liked_writers)

        return (
            Book.objects.filter(
                Q(grade=user_profile.grade)
                | Q(school_name=user_profile.school_name),
                similarity_q,
            )
            .exclude(id__in=liked_ids)
            .only(
                "title",
                "description",
                "school_name",
                "publisher",
                "slug",
                "is_downloadable",
                "file",
            )
            .order_by("-likes_count")
        )

    should = []

    if liked_schools:
        should.append({"terms": {"school_name": list(liked_schools)}})

    if liked_publishers:
        should.append({"terms": {"publisher": list(liked_publishers)}})

    if liked_writers:
        should.append({"terms": {"writer": list(liked_writers)}})

    search = (
        BookDocument.search()
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

def get_filtered_books_by_params(
    grades: List[str],
    types: List[str],
    is_downloadable: bool,
    is_not_downloadable: bool,
) -> QuerySet[Book]:
    """
    Retrieve books filtered by various criteria.

    Args:
        grades (List[str]): List of grades.
        types (List[str]): List of book categories/tags.
        is_downloadable (bool): Include downloadable books.
        is_not_downloadable (bool): Include non-downloadable books.

    Returns:
        QuerySet[Book]: The filtered Book queryset.

    document by AI
    """

    if not settings.PRODUCTION:
        qs = get_books_for_list()

        if grades:
            grade_q = Q()
            for grade in grades:
                grade_q |= Q(grade=grade)
            qs = qs.filter(grade_q)

        if types:
            type_q = Q()
            for t in types:
                type_q |= Q(tags__icontains=t)
            qs = qs.filter(type_q)

        if is_downloadable or is_not_downloadable:
            download_q = Q()
            if is_downloadable:
                download_q |= Q(is_downloadable=True)
            if is_not_downloadable:
                download_q |= Q(is_downloadable=False)
            qs = qs.filter(download_q)

        return qs

    search = BookDocument.search()

    if grades:
        search = search.filter("terms", grade=grades)

    if types:
        for t in types:
            search = search.filter(
                "match",
                tags=t,
            )

    if is_downloadable or is_not_downloadable:
        values = []
        if is_downloadable:
            values.append(True)
        if is_not_downloadable:
            values.append(False)

        search = search.filter(
            "terms",
            is_downloadable=values,
        )

    return search.to_queryset()

def get_book_by_slug(slug: str) -> Book:
    """
    Retrieve a book by its slug.

    Args:
        slug (str): The unique slug of the book.

    Returns:
        Book: The matching Book instance.

    document by AI
    """
    try:
        return Book.objects.get(slug=slug)
    except:
        return None

def get_book_by_id(book_id: int) -> Book:
    """
    Retrieve a book by its database ID.

    Args:
        book_id (int): The database ID.

    Returns:
        Book: The matching Book instance.

    document by AI
    """
    return Book.objects.get(id=book_id)

def search_books_database(query: str):
    """
        Search books by default django ORM.
    
        Args:
            query (str): The search query.
    
        Returns:
            QuerySet[Question]: The matching Question queryset.
    
        document by AI
    """
    return Book.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(writer__icontains=query) |
        Q(tags__icontains=query) |
        Q(school_name__icontains=query) |
        Q(publisher__icontains=query) | 
        Q(address_icontains=query)
    )

def search_books_elasticsearch(query: str):
    """
        Search books by Elasticsearch.
        
        Args:
            query (str): The search query.
        
        Returns:
            QuerySet[Question]: The matching Question queryset.
        
        document by AI
    """
    search = (
        BookDocument.search()
        .query(
            "multi_match",
            query=query,
            fields=[
                "title",
                "description",
                "writer",
                "tags",
                "school_name",
                "publisher",
                "address"
            ],
            fuzziness="AUTO",
        )
    )

    return search.to_queryset()
