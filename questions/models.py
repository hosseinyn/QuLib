from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import FileExtensionValidator

# Create your models here.
class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(null=False , blank=False , unique=True)
    slug = models.SlugField(null=True , blank=True , db_index=True)
    description = models.TextField(null=False , blank=False , db_index=True)
    school_name = models.CharField(null=False , blank=False , db_index=True)
    grade = models.CharField(null=False , blank=False , db_index=True)
    is_solved = models.BooleanField(null=False , db_index=True)
    difficulty = models.CharField(null=False , blank=False , default="راحت" , db_index=True)
    file = models.FileField(null=False , validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            )
        ])
    likes_count = models.IntegerField(null=False , default=0)
    tags = models.CharField(null=False , blank=False , db_index=True)
    writer = models.CharField(null=False , blank=False , db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('question_page', kwargs={'slug': self.slug})

    class Meta:
        indexes = [
            models.Index(fields=["grade", "-likes_count"], name="question_grade_likes_idx"),
            models.Index(fields=["school_name", "-likes_count"], name="question_school_likes_idx"),
            models.Index(fields=["difficulty", "-likes_count"], name="question_diff_likes_idx"),
        ]
    
    def __str__(self):
        return self.title