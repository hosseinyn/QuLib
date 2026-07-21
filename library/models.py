from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import FileExtensionValidator

# Create your models here.
class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(null=False , blank=False , unique=True)
    slug = models.SlugField(null=True , blank=True , db_index=True)
    description = models.TextField(null=False , blank=False , db_index=True)
    school_name = models.CharField(null=False , blank=False , db_index=True)
    grade = models.CharField(null=False , blank=False , db_index=True)
    publisher = models.CharField(null=False , blank=False , default="نامشخص" , db_index=True)
    file = models.FileField(null=True , blank=True , validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            )
        ])
    likes_count = models.IntegerField(null=False , default=0)
    tags = models.CharField(null=False , blank=False , db_index=True)
    writer = models.CharField(null=False , blank=False , db_index=True)
    is_downloadable = models.BooleanField(null=False , default=False , db_index=True)
    address = models.TextField(null=True , blank=True)

    def save(self , *args, **kwargs):
        self.slug = slugify(self.title , allow_unicode=True)
        return super().save()

    def get_absolute_url(self):
        return reverse('book_page', kwargs={'slug': self.slug})

    class Meta:
        indexes = [
            models.Index(fields=["grade", "-likes_count"], name="book_grade_likes_idx"),
            models.Index(fields=["school_name", "-likes_count"], name="book_school_likes_idx"),
        ]
    
    def __str__(self):
        return self.title