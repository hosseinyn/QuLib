from django.urls import path

from .views import index , about , partnership , contact , faq , reviews , leaderboard , terms , privacy

urlpatterns = [
    path('' , view=index , name="صفحه خانه"),
    path('about/' , view=about , name="درباره ما"),
    path('partnership/' , view=partnership , name="همکاری با ما"),
    path('contact/' , view=contact , name="تماس با ما"),
    path('faq/' , view=faq , name="سوالات متداول"),
    path('reviews/' , view=reviews , name="نظرات مشتریان"),
    path('leaderboard/' , view=leaderboard , name="لیدربرد"),
    path('terms/' , view=terms , name="قوانین و مقررات"),
    path('privacy-policy/' , view=privacy , name="سیاست های حفظ حریم خصوصی"),
]
