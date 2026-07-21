from django.contrib import admin

from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['school_name', 'grade', 'publisher' , 'writer' , 'tags' , 'is_downloadable' , 'likes_count']
    list_filter = ['grade' , 'publisher' , 'tags']
    search_fields = ['school_name' , 'publisher' , 'writer' , 'description' , 'title' , 'address']
