from django.contrib.sitemaps import Sitemap
from questions.models import Question
from library.models import Book

class QuestionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Question.objects.all()

class BookSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return Book.objects.all()