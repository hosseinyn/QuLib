from django.urls import path

from .views import books_bank , books_search , book_page , like_book , unlike_book , delete_comment , edit_comment

urlpatterns = [
    path('' , view=books_bank),
    path('search/' , view=books_search),
    path('book/<str:slug>' , view=book_page , name="book_page"),
    path('like/' , view=like_book),
    path('unlike/' , view=unlike_book),
    path('edit-comment/' , view=edit_comment),
    path('delete-comment/' , view=delete_comment)
]