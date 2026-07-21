from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Question

# ایندکس مدل نمونه سوالات
@registry.register_document
class QuestionDocument(Document):
    class Index:
        name = "questions"

    class Django:
        model = Question

        fields = [
            "title",
            "description",
            "school_name",
            "writer",
            "tags",
            "grade",
            "difficulty",
            "likes_count"
        ]