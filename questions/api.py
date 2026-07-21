from typing import List

from ninja import NinjaAPI, Query
from ninja.pagination import paginate, PageNumberPagination

from django.conf import settings
from django.db.models import Q

from questions.models import Question
from library.models import Book

from questions.documents import QuestionDocument
from library.documents import BookDocument

from .schema import (
    QuestionSchema,
    SearchSchema,
    BookSchema,
    QuestionResponseSchema,
    BookResponseSchema,
)


api = NinjaAPI(
    title="API کولیب",
    version="1.0.0",
    docs_url="/qulib-docs",
    openapi_url="/openapi.json",
)


QUESTION_FIELDS = (
    "title",
    "description",
    "school_name",
    "grade",
    "is_solved",
    "difficulty",
    "likes_count",
    "tags",
    "writer",
)


BOOK_FIELDS = (
    "title",
    "description",
    "school_name",
    "grade",
    "publisher",
    "likes_count",
    "tags",
    "writer",
)


@api.get(
    "/questions",
    response=List[QuestionResponseSchema]
)
@paginate(PageNumberPagination)
def get_questions(
    request,
    params: QuestionSchema = Query(...),
    search: SearchSchema = Query(...)
):

    grades = []

    if params.is_hashtom:
        grades.append("هشتم")

    if params.is_haftom:
        grades.append("هفتم")

    if params.is_nohom:
        grades.append("نهم")


    if settings.PRODUCTION:

        search_es = QuestionDocument.search()


        if search.query:
            search_es = search_es.query(
                "multi_match",
                query=search.query,
                fields=[
                    "title",
                    "description",
                    "writer",
                    "school_name",
                    "tags",
                ],
                fuzziness="AUTO",
            )


        if grades:
            search_es = search_es.filter(
                "terms",
                grade=grades,
            )


        tags = []

        if params.is_nobat1:
            tags.append("نوبت1")

        if params.is_nobat2:
            tags.append("نوبت2")

        if params.is_mostamar:
            tags.append("مستمر")

        if params.is_payani:
            tags.append("پایانی")


        for tag in tags:
            search_es = search_es.filter(
                "match",
                tags=tag,
            )


        difficulty = []

        if params.is_rahat:
            difficulty.append("راحت")

        if params.is_motavasset:
            difficulty.append("متوسط")

        if params.is_sakht:
            difficulty.append("سخت")

        if difficulty:
            search_es = search_es.filter(
                "terms",
                difficulty=difficulty,
            )

        qs = search_es.to_queryset()

    else:

        qs = Question.objects.all()

        if search.query:
            qs = qs.filter(
                description__icontains=search.query
            )

        if grades:
            qs = qs.filter(
                grade__in=grades
            )

        nobat_filter = Q()

        if params.is_nobat1:
            nobat_filter |= Q(
                tags__icontains="نوبت1"
            )

        if params.is_nobat2:
            nobat_filter |= Q(
                tags__icontains="نوبت2"
            )

        if nobat_filter:
            qs = qs.filter(nobat_filter)

        time_filter = Q()

        if params.is_mostamar:
            time_filter |= Q(
                tags__icontains="مستمر"
            )

        if params.is_payani:
            time_filter |= Q(
                tags__icontains="پایانی"
            )

        if time_filter:
            qs = qs.filter(time_filter)


        difficulty_filter = Q()

        if params.is_rahat:
            difficulty_filter |= Q(difficulty="راحت")

        if params.is_motavasset:
            difficulty_filter |= Q(difficulty="متوسط")

        if params.is_sakht:
            difficulty_filter |= Q(difficulty="سخت")

        if difficulty_filter:
            qs = qs.filter(difficulty_filter)


    return qs.values(*QUESTION_FIELDS)

@api.get(
    "/books",
    response=List[BookResponseSchema]
)
@paginate(PageNumberPagination)
def get_books(
    request,
    params: BookSchema = Query(...),
    search: SearchSchema = Query(...)
):

    grades = []

    if params.is_hashtom:
        grades.append("هشتم")

    if params.is_haftom:
        grades.append("هفتم")

    if params.is_nohom:
        grades.append("نهم")


    if settings.PRODUCTION:

        search_es = BookDocument.search()

        if search.query:
            search_es = search_es.query(
                "multi_match",
                query=search.query,
                fields=[
                    "title",
                    "description",
                    "writer",
                    "school_name",
                    "tags",
                ],
                fuzziness="AUTO",
            )

        if grades:
            search_es = search_es.filter(
                "terms",
                grade=grades,
            )


        tags = []

        if params.is_amoozeshi:
            tags.append("آموزشی")

        if params.is_emtahani:
            tags.append("امتحانی")

        if params.is_gambegam:
            tags.append("گام به گام")

        for tag in tags:
            search_es = search_es.filter(
                "match",
                tags=tag,
            )

        qs = search_es.to_queryset()

    else:

        qs = Book.objects.all()

        if search.query:
            qs = qs.filter(
                description__icontains=search.query
            )

        if grades:
            qs = qs.filter(
                grade__in=grades
            )

        type_filter = Q()

        if params.is_amoozeshi:
            type_filter |= Q(
                tags__icontains="آموزشی"
            )


        if params.is_emtahani:
            type_filter |= Q(
                tags__icontains="امتحانی"
            )


        if params.is_gambegam:
            type_filter |= Q(
                tags__icontains="گام به گام"
            )

        if type_filter:
            qs = qs.filter(type_filter)

    return qs.values(*BOOK_FIELDS)