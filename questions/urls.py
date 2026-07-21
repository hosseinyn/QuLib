from django.urls import path

from .views import questions_bank , questions_search , question_page , like_question , unlike_question , convert_pdf_to_word , delete_comment , process_pdf , process_image , edit_comment , convert_pdf_to_word_status , process_pdf_status , process_image_status

urlpatterns = [
    path('' , view=questions_bank),
    path('search/' , view=questions_search),
    path('question/<str:slug>' , view=question_page , name="question_page"),
    path('like/' , view=like_question),
    path('unlike/' , view=unlike_question),
    path('convert-to-word/' , view=convert_pdf_to_word),
    path('convert-to-word-status/<str:task_id>' , view=convert_pdf_to_word_status),
    path('delete-comment/' , view=delete_comment),
    path('edit-comment/' , view=edit_comment),
    path('process-pdf/' , view=process_pdf),
    path('process-pdf-status/<str:task_id>' , view=process_pdf_status),
    path('process-image/' , view=process_image),
    path('process-image-status/<str:task_id>' , view=process_image_status),
]