from django import forms

import re
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(required=True , widget=forms.EmailInput({"placeholder" : "آدرس ایمیل خود را وارد کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="ایمیل شما ")

    password = forms.CharField(required=True , widget=forms.PasswordInput(attrs={"placeholder" : "گذرواژه خود را وارد کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="گذرواژه شما " , min_length=6 , max_length=40)


class SignupForm(forms.Form):
    email = forms.EmailField(required=True , widget=forms.EmailInput({"placeholder" : "آدرس ایمیل خود را وارد کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="ایمیل شما ")

    password = forms.CharField(required=True , widget=forms.PasswordInput(attrs={"placeholder" : "گذرواژه خود را وارد کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="گذرواژه شما " , min_length=6 , max_length=40)

    confirm_password = forms.CharField(required=True , widget=forms.PasswordInput(attrs={"placeholder" : "گذرواژه خود را تکرار کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="تکرار گذرواژه شما " , min_length=6 , max_length=40)


    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("رمز عبور ها یکسان نیستند")

        return confirm_password
    

CLASS_OPTIONS = [
    ('هفتم' , 'هفتم'),
    ('هشتم' , 'هشتم'),
    ('نهم' , 'نهم')
]

import re
from django.core.exceptions import ValidationError

def username_validator(value):
    pattern = r'^[A-Za-z0-9_]+$'

    if not re.match(pattern, value):
        raise ValidationError(
            "نام کاربری فقط می‌تواند شامل حروف انگلیسی، اعداد و _ باشد."
        )

class EditForm(forms.Form):
    username = forms.CharField(required=True , label="نام کاربری :" , widget=forms.TextInput(attrs={"placeholder" : "نام کاربری جدید را وارد کنید..." , "class" : "h-full px-2 w-full outline-none bg-transparent"}) , validators=[username_validator] , min_length=3 , max_length=12)

    school_name = forms.CharField(required=True , label="نام مدرسه..." , widget=forms.TextInput(attrs={"placeholder" : "نام مدرسه را وارد کنید..." , "class" : "h-full px-2 w-full outline-none bg-transparent"}), min_length=5 , max_length=30)

    grade = forms.ChoiceField(required=True , label="پایه تحصیلی : " , widget=forms.Select(attrs={"class" : "h-full px-2 w-full outline-none bg-transparent"}) , choices=CLASS_OPTIONS)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(required=True , label="رمز عبور قبلی : " , widget=forms.PasswordInput(attrs={"placeholder" : "رمز عبور قبلی را وارد کنید..." , "class" : "h-full px-4 w-full outline-none bg-transparent"}) , min_length=6 , max_length=40)

    new_password = forms.CharField(required=True , label="پسورد جدید :" , widget=forms.PasswordInput(attrs={"placeholder" : "پسورد جدید را وارد کنید..." , "class" : "h-full px-4 w-full outline-none bg-transparent"}) , min_length=6 , max_length=40)

    confirm_password = forms.CharField(required=True , label="تکرار رمز عبور جدید :" , widget=forms.PasswordInput(attrs={"placeholder" : "تکرار رمز عبور جدید..." , "class" : "h-full px-4 w-full outline-none bg-transparent"}) , min_length=6 , max_length=40)

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("رمز عبور ها یکسان نیستند")

        return confirm_password
    

class RecoveryPasswordForm(forms.Form):

    password = forms.CharField(required=True , widget=forms.PasswordInput(attrs={"placeholder" : "گذرواژه خود را وارد کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="گذرواژه شما " , min_length=6 , max_length=40)

    confirm_password = forms.CharField(required=True , widget=forms.PasswordInput(attrs={"placeholder" : "گذرواژه خود را تکرار کنید..." , "class" : "bg-transparent text-gray-500/80 placeholder-gray-500/80 outline-none text-sm w-full h-ful"}) , label="تکرار گذرواژه شما " , min_length=6 , max_length=40)


    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("رمز عبور ها یکسان نیستند")

        return confirm_password

class DeleteAccountForm(forms.Form):
    reason = forms.CharField(required=True , min_length=2 , max_length=470 , widget=forms.Textarea(attrs={"class" : "border border-gray-200 rounded-lg p-4 outline-none resize-none w-11/12" , "placeholder" : "دلیل حذف حساب کاربریت رو وارد کن..."}))