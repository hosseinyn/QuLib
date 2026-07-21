from django.test import TestCase

from library.models import Book
from library.repositories.book_repository import (
    get_book_by_slug,
    get_filtered_books_by_params,
)


class BookRepositoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(
            title="ریاضی هشتم",
            description="کتاب آموزش ریاضی",
            grade="8",
            publisher="خیلی سبز",
            school_name="نمونه",
            tags="کمک آموزشی,آموزشی",
            is_downloadable=True,
        )

        cls.book2 = Book.objects.create(
            title="علوم نهم",
            description="کتاب علوم پایه نهم",
            grade="9",
            publisher="گاج",
            school_name="شاهد",
            tags="درسی",
            is_downloadable=False,
        )

    # تست دریافت کتاب با اسلاگ
    def test_get_book_by_slug(self):

        book = get_book_by_slug("ریاضی-هشتم")

        self.assertEqual(book.id, self.book1.id)

    # تست برنگشتن کتاب با اسلاگ نامعتبر
    def test_get_invalid_book_by_slug(self):

        book = get_book_by_slug("unknown")

        self.assertIsNone(book)
