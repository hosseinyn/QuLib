from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout

from .forms import LoginForm, SignupForm, EditForm, ChangePasswordForm, RecoveryPasswordForm , DeleteAccountForm

from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit

from .services.auth_service import (
    process_login, process_signup, process_change_password, 
    process_forgot_password, get_recovery_password_status, process_recovery_password
)
from .services.profile_service import (
    get_user_panel_data, get_account_data, process_delete_account, process_edit_profile
)
from user.repositories.user_profile_repository import get_user_profile

# Create your views here.
@ratelimit(key='ip', rate='10/h')
def login(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            form = LoginForm
            return render(request, 'login.html', {"form": form})
        
        elif request.method == "POST":
            form = LoginForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                success, message = process_login(request, email, password)

                if success:
                    return redirect("/user/panel/")
                else:
                    return render(request, 'login.html', {"form": form, "error": message})
            else:
                return render(request, 'login.html', {"form": form})
    else:
        return redirect("/user/panel/")
        
@ratelimit(key='ip', rate='2/d')
def signup(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            form = SignupForm
            return render(request, 'signup.html', {"form": form})
        
        elif request.method == "POST":
            form = SignupForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]

                success, message = process_signup(email, password)

                if success:
                    return redirect("/user/login/")
                else:
                    return render(request, 'signup.html', {"form": form, "error": message})
            else:
                return render(request, 'signup.html', {"form": form})
    else:
        return redirect("/user/panel/")

@login_required
def panel(request):
    if request.user.is_authenticated:
        data = get_user_panel_data(request.user)
        return render(request, "panel.html", data)
    else:
        return redirect("/user/login/")
    
def user_account(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return redirect("/user/panel/")
    
    data = get_account_data(username)
    if data:
        return render(request, "user.html", data)
    else:
        return redirect("/")

@login_required
def logout(request):
    django_logout(request)
    return redirect("/")

@login_required
@ratelimit(key='ip', rate='7/h')
def edit(request):
    if request.method == "GET":
        user_profile = get_user_profile(request.user)
        form = EditForm(
            initial={
                "username": request.user.username,
                "school_name": user_profile.school_name,
                "grade": user_profile.grade
            }
        )
        return render(request, "edit.html", {"form": form})
    
    elif request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            school_name = form.cleaned_data["school_name"]
            grade = form.cleaned_data["grade"]
            profile_picture_id = request.POST.get("avatar")

            success, message = process_edit_profile(
                request.user, username, school_name, grade, profile_picture_id
            )

            if success:
                return redirect("/user/panel/")
            else:
                return render(request, "edit.html", {"form": form, "error": message})
        else:
            return render(request, "edit.html", {"form": form})

@login_required
@ratelimit(key='ip', rate='7/h')
def change_password(request):
    if request.method == "GET":
        form = ChangePasswordForm
        return render(request, "change_password.html", {"form": form})
    
    elif request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            success, message = process_change_password(request, old_password, new_password)

            if success:
                django_logout(request)
                return redirect("/user/login/")
            else:
                return render(request, "change_password.html", {"form": form, "error": message})
        else:
            return render(request, "change_password.html", {"form": form})

@login_required
def delete_account(request):
    if request.method == "GET":
        form = DeleteAccountForm()
        return render(request, "delete.html" , {"form" : form})
    elif request.method == "POST":
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            process_delete_account(request.user.username , reason)
            django_logout(request)
            return redirect("/")
        else :
            form = DeleteAccountForm()
            return render(request, "delete.html" , {"form" : form})
        
@ratelimit(key='ip', rate='5/d')
def forgot_password(request):
    if not request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "forgot_password.html")
        elif request.method == "POST":
            email = request.POST.get("email")
            process_forgot_password(email)
            return redirect("/user/login/")
    else:
        return redirect("/user/panel/")

def recovery_password(request, token):
    if request.user.is_authenticated:
        return redirect("/user/panel/")

    is_valid, record = get_recovery_password_status(token)

    if not is_valid:
        return redirect("/")

    if request.method == "GET":
        form = RecoveryPasswordForm()
        return render(request, "recovery_password.html", {"form": form})

    if request.method == "POST":
        form = RecoveryPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["password"]
            process_recovery_password(request, record, new_password)
            return redirect("/user/panel/")

        return render(request, "recovery_password.html", {"form": form})

    return redirect("/")