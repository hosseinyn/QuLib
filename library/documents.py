from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Book

# ایندکس مدل کتاب ها
@registry.register_document
class BookDocument(Document):
    class Index:
        name = "books"

    class Django:
        model = Book

        fields = [
            "title",
            "description",
            "school_name",
            "publisher",
            "writer",
            "tags",
            "address",
            "grade",
            "is_downloadable",
            "likes_count"
        ]