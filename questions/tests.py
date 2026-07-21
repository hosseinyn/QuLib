from django.test import TestCase

from questions.models import Question
from questions.repositories.question_repository import (
    get_filtered_questions_by_params,
    get_question_by_slug,
)

class QuestionRepositoryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.q1 = Question.objects.create(
            title="ریاضی",
            description="نمونه سوال ریاضی",
            grade="8",
            difficulty="easy",
            tags="نوبت اول,میان ترم",
            school_name="نمونه",
            is_solved=False
        )

        cls.q2 = Question.objects.create(
            title="علوم",
            description="نمونه سوال علوم",
            grade="9",
            difficulty="hard",
            tags="نوبت دوم,پایانی",
            school_name="شاهد",
            is_solved=False
        )

    # تست دریافت سوال با اسلاگ
    def test_get_question_by_slug(self):

        question = get_question_by_slug("ریاضی")

        self.assertEqual(question.id, self.q1.id)

    # تست برنگشتن سوال با اسلاگ نامعتبر
    def test_get_question_by_invalid_slug(self):

        question = get_question_by_slug("unknown")

        self.assertIsNone(question)