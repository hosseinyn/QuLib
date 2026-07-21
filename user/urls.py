from django.urls import path

from .views import login , signup , panel , logout , edit , change_password , delete_account , forgot_password , recovery_password , user_account

urlpatterns = [
    path('login/' , view=login , name="ورود به حساب کاربری"),
    path('signup/' , view=signup , name="ثبت نام"),
    path('panel/' , view=panel , name="داشبورد"),
    path('logout/' , view=logout , name="خروج"),
    path('edit/' , view=edit , name="ویرایش حساب کاربری"),
    path('change-password/' , view=change_password , name="تغییر رمز عبور"),
    path('delete/' , view=delete_account , name="حذف حساب کاربری"),
    path('forgot-password/' , view=forgot_password , name="فراموشی رمز عبور"),
    path('recovery-password/<str:token>/' , view=recovery_password , name="بازیابی پسورد"),
    path('person/<str:username>/' , view=user_account , name="اکانت یک کاربر"),
]