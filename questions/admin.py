from django.contrib import admin

from .models import Question

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title' , 'school_name', 'grade', 'difficulty' , 'writer' , 'tags' , 'likes_count']
    list_filter = ['grade' , 'difficulty' , 'tags' , 'is_solved']
    search_fields = ['writer' , 'school_name' , 'title' , 'description']