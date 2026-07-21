from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
from django.http import Http404

from .services.question_service import (
    get_filtered_questions, search_questions, get_question_page_data,
    process_question_comment, process_edit_comment, process_delete_comment,
    process_like_question, process_unlike_question, get_edit_comment_data
)
from .repositories.question_repository import get_questions_for_list
from .tasks import convert_pdf, extract_text_from_uploaded_pdf, extract_image_text
from celery.result import AsyncResult
from django.views.decorators.csrf import csrf_exempt
import tempfile

def questions_bank(request):
    if request.method == "GET":
        page_number = request.GET.get("page")

        use_cache = page_number in (None, "", "1")

        if use_cache:
            if request.user.is_authenticated:
                cache_key = f"questions:first_page:user:{request.user.id}"
            else:
                cache_key = "questions:first_page:anonymous"

            qs = cache.get(cache_key)

            if qs is None:
                qs = list(get_questions_for_list(user=request.user))
                cache.set(cache_key, qs, 60 * 5)
        else:
            qs = list(get_questions_for_list(user=request.user))

        paginator = Paginator(qs, 12)
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "questions.html",
            {
                "questions": page_obj.object_list,
                "page_obj": page_obj,
            },
        )

    elif request.method == "POST":
        qs = get_filtered_questions(request.POST)

        paginator = Paginator(qs, 12)
        page_obj = paginator.get_page(request.GET.get("page"))

        return render(
            request,
            "questions.html",
            {
                "questions": page_obj.object_list,
                "page_obj": page_obj,
            },
        )

def questions_search(request):
    search_query = request.GET.get("q", "")
    questions = search_questions(search_query)
    
    paginator = Paginator(questions, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "questions.html", {"questions": page_obj.object_list, "page_obj": page_obj, "search_query": search_query})

def question_page(request, slug):
    if request.method == "GET":
        data = get_question_page_data(request.user, slug)
        if not data:
            raise Http404("Question not found")
        return render(request, "question_page.html", data)
    
    elif request.method == "POST":
        if request.user.is_authenticated:
            message = request.POST.get("message")
            rate = request.POST.get("rating")
            
            _, data = process_question_comment(request.user, slug, message, rate)
            return render(request, "question_page.html", data)
        else:
            return redirect("/user/login/")

@login_required
@ratelimit(key='ip', rate='10/m')
def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        question_slug = request.POST.get("question_slug")
        process_delete_comment(request.user, comment_id)
        
        return redirect(f"/questions/question/{question_slug}")

@login_required
@ratelimit(key='ip', rate='10/m')
def edit_comment(request):
    if request.method == "POST":
        method = request.POST.get("_method")
        if method == "get":
            question_slug = request.POST.get("question_slug")
            comment_id = request.POST.get("comment_id")
            data = get_edit_comment_data(request.user, question_slug, comment_id)
            return render(request, "question_page.html", data)
    
        elif method == "post":
            comment_id = request.POST.get("comment_id")
            message = request.POST.get("message")
            rate = request.POST.get("rating")
            question_slug = request.POST.get("question_slug")

            _, data = process_edit_comment(request.user, question_slug, comment_id, message, rate)
            return redirect(f"/questions/question/{question_slug}")
    else :
        return redirect("/questions/")

@login_required
@ratelimit(key='ip', rate='20/m')
def like_question(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        process_like_question(request.user, question_id)

        ref = request.META.get("HTTP_REFERER")
        if ref:
            path = urlparse(ref).path
            return redirect(path)
        return redirect("/")

@login_required
@ratelimit(key='ip', rate='20/m')
def unlike_question(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        process_unlike_question(request.user, question_id)

        ref = request.META.get("HTTP_REFERER")
        if ref:
            path = urlparse(ref).path
            return redirect(path)
        return redirect("/")

@login_required
@ratelimit(key='ip', rate='10/m')
@csrf_exempt
def convert_pdf_to_word(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")

        task = convert_pdf.delay(question_id)
        return JsonResponse({
            "task_id": task.id
        })

def convert_pdf_to_word_status(request, task_id):

    task = AsyncResult(task_id)

    if task.ready():

        response = HttpResponse(
                    task.result["word_io"],
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
        
        response['Content-Disposition'] = f'attachment; filename="{task.result["name"]}.docx"'
        
        return response

    return JsonResponse({
        "status": "processing"
    })

@login_required
@ratelimit(key='ip', rate='10/m')
@csrf_exempt
def process_pdf(request):
    if request.method == "GET":
        return render(request, "process_pdf_form.html")
    elif request.method == "POST":
        pdf_file = request.FILES.get("pdf_file")

        if pdf_file.size > 5 * 1024 * 1024:
            return render(request, "process_pdf_form.html", {"error": "حداکثر حجم مجاز فایل 5 مگابایت است."})

        file_start = pdf_file.read(5)
        if file_start != b"%PDF-":
            return render(request, "process_pdf_form.html", {"error": "فایل شما معتبر نیست."})
        
        pdf_file.seek(0)
        
        if pdf_file.content_type != "application/pdf":
            return render(request, "process_pdf_form.html", {"error": "فایل شما معتبر نیست."})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            for chunk in pdf_file.chunks():
                tmp.write(chunk)
            temp_path = tmp.name
        
        task = extract_text_from_uploaded_pdf.delay(temp_path)

        return JsonResponse({
                "task_id": task.id
        })

def process_pdf_status(request, task_id):

    task = AsyncResult(task_id)

    if task.ready():
        pdf_status = task.result["status"]
        if pdf_status != False:
            pdf_text = task.result["text"]
            return render(request, "process_pdf_form.html", {"text": pdf_text})
        else :
            return render(request, "process_pdf_form.html", {"error": "پردازش فایل موفقیت آمیز نبود."})

    return JsonResponse({
        "status": "processing"
    })


@login_required
@ratelimit(key='ip', rate='10/m')
@csrf_exempt
def process_image(request):
    if request.method == "GET":
        return render(request, "process_image_form.html")
    elif request.method == "POST":
        image_file = request.FILES.get("image_file")

        if image_file.size > 5 * 1024 * 1024:
            return render(request, "process_image_form.html", {"error": "حداکثر حجم مجاز فایل 5 مگابایت است."})

        file_start = image_file.read(8)

        if file_start.startswith(b'\x89PNG\r\n\x1a\n'):
            pass
        elif file_start.startswith(b'\xff\xd8\xff'):
            pass
        else:
            return render(request, "process_image_form.html", {"error": "فایل شما معتبر نیست."})

        image_file.seek(0)

        if image_file.content_type not in ["image/png", "image/jpeg"]:
            return render(request, "process_image_form.html", {"error": "فرمت فایل باید PNG یا JPEG باشد."})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpeg") as tmp:
            for chunk in image_file.chunks():
                    tmp.write(chunk)
            temp_path = tmp.name
        
        task = extract_image_text.delay(temp_path)

        return JsonResponse({
                "task_id": task.id
        })

def process_image_status(request, task_id):

    task = AsyncResult(task_id)

    if task.ready():
        image_status = task.result["status"]
        if image_status != False:
            image_text = task.result["text"]
            return render(request, "process_image_form.html", {"text": image_text})
        else :
            return render(request, "process_image_form.html", {"error": "پردازش فایل موفقیت آمیز نبود."})

    return JsonResponse({
        "status": "processing"
    })