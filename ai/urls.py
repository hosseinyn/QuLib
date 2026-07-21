from django.urls import path

from .views import ai_chat , difficulty_detector , create_same_question , solve_text , new_chat , delete_chat , chat , difficulty_detector_status , create_same_question_status , solve_text_status

urlpatterns = [
    path('' , view=ai_chat , name="کولیب AI"),
    path('difficulty-detector/' , view=difficulty_detector),
    path('difficulty-detector-status/<str:task_id>' , view=difficulty_detector_status),
    path('create-same-question/' , view=create_same_question),
    path('create-same-question-status/<str:task_id>' , view=create_same_question_status),
    path('solve-text/' , view=solve_text),
    path('solve-text-status/<str:task_id>' , view=solve_text_status),
    path('new-chat/' , view=new_chat),

    path('chat/<str:uuid>/' , view=chat),
    path('chat/<str:uuid>/delete/' , view=delete_chat),
]