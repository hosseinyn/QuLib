from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from .repositories.chat_repository import get_all_chats , create_new_chat , delete_chat_by_uuid , get_chat_by_uuid
from django.http import JsonResponse
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt

from .tasks import (
    detect_difficulty,
    generate_same_questions,
    solve_math_text,
)

def _get_user_rate_key(group, request):
    return str(request.user.id)

@login_required
@ratelimit(key=_get_user_rate_key, rate="10/d", method="POST", block=True)
def ai_chat(request):
    if request.method == "GET":
        chats = get_all_chats(request.user)
        return render(request, "ai_chat.html" , {"chats" : chats})
    
@login_required
@ratelimit(key=_get_user_rate_key, rate="17/d", method="POST", block=True)
def new_chat(request):
    if request.method == "POST":
        create_new_chat(request.user)
        return redirect("/qulib-ai/")
    else :
        return redirect("/qulib-ai/")

@login_required
def delete_chat(request , uuid):
    if request.method == "POST":
        delete_chat_by_uuid(request.user , uuid=uuid)
        return redirect("/qulib-ai/")
    else :
        return redirect("/qulib-ai/")

@login_required
def chat(request , uuid):
    if request.method == "GET":
        chat = get_chat_by_uuid(request.user , uuid)
        if chat:
            chats = get_all_chats(request.user)
            default = request.GET.get("default") or ""
            return render(request , "ai_chat.html" , {"chats" : chats , "chat" : chat , "default" : default})
        else :
            return redirect("/qulib-ai/")

@login_required
@ratelimit(key=_get_user_rate_key, rate="50/d", method="POST", block=True)
@csrf_exempt
def difficulty_detector(request):
    if request.method == "GET":
        return redirect("/questions/process-pdf/")
    if request.method == "POST":
        text = request.POST.get("text")
        from_where = request.POST.get("from")
        
        template_name = "process_image_form.html"
        if from_where == "pdf":
            template_name = "process_pdf_form.html"

        task = detect_difficulty.delay(text , template_name)
        return JsonResponse({ "task_id": task.id })

@login_required
@ratelimit(key=_get_user_rate_key, rate="50/d", method="POST", block=True)
def difficulty_detector_status(request , task_id):
    task = AsyncResult(task_id)

    if task.ready():
        response = task.result["response"]
        if response != "__AI_ERROR__":
            template_name = task.result["template_name"]
            text = task.result["text"]
            return render(request, template_name, {"text": text, "ai_response": response})
        else :
            return render(request , "ai_error.html")

    return JsonResponse({
        "status": "processing"
    })

@login_required
@ratelimit(key=_get_user_rate_key, rate="14/d", method="POST", block=True)
@csrf_exempt
def create_same_question(request):
    if request.method == "GET":
        return redirect("/questions/process-pdf/")
    if request.method == "POST":
        text = request.POST.get("text")
        from_where = request.POST.get("from")
        
        template_name = "process_image_form.html"
        if from_where == "pdf":
            template_name = "process_pdf_form.html"

        task = generate_same_questions.delay(text , template_name)

        return JsonResponse({ "task_id": task.id })

@login_required
@ratelimit(key=_get_user_rate_key, rate="14/d", method="POST", block=True)
def create_same_question_status(request , task_id):
    task = AsyncResult(task_id)

    if task.ready():
        response = task.result["response"]
        if response != "__AI_ERROR__":
            template_name = task.result["template_name"]
            text = task.result["text"]
            return render(request, template_name, {"text": text, "ai_question": response})
        else :
            return render(request , "ai_error.html")

    return JsonResponse({
        "status": "processing"
    })

@login_required
@ratelimit(key=_get_user_rate_key, rate="14/d", method="POST", block=True)
@csrf_exempt
def solve_text(request):
    if request.method == "GET":
        return redirect("/questions/process-pdf/")
    if request.method == "POST":
        text = request.POST.get("text")
        from_where = request.POST.get("from")
        
        template_name = "process_image_form.html"
        if from_where == "pdf":
            template_name = "process_pdf_form.html"

        task = solve_math_text.delay(text , template_name)

        return JsonResponse({ "task_id": task.id })

@login_required
@ratelimit(key=_get_user_rate_key, rate="14/d", method="POST", block=True)
def solve_text_status(request , task_id):
    task = AsyncResult(task_id)

    if task.ready():
        response = task.result["response"]
        if response != "__AI_ERROR__":
            template_name = task.result["template_name"]
            text = task.result["text"]
            return render(request, template_name, {"text": text, "ai_solve": response})
        else :
            return render(request , "ai_error.html")

    return JsonResponse({
        "status": "processing"
    })