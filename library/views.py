from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
from django.http import Http404

from .services.book_service import (
    get_filtered_books, search_books, get_book_page_data, 
    process_book_comment, process_delete_comment, process_like_book, process_unlike_book , get_edit_comment_data , process_edit_comment
)
from .repositories.book_repository import get_books_for_list, get_book_by_id

def books_bank(request):
    if request.method == "GET":
        page_number = request.GET.get("page")

        use_cache = page_number in (None, "", "1")

        if use_cache:
            if request.user.is_authenticated:
                cache_key = f"books:first_page:user:{request.user.id}"
            else:
                cache_key = "books:first_page:anonymous"

            qs = cache.get(cache_key)

            if qs is None:
                qs = list(get_books_for_list(user=request.user))
                cache.set(cache_key, qs, 60 * 5)
        else:
            qs = list(get_books_for_list(user=request.user))

        paginator = Paginator(qs, 12)
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "books.html",
            {
                "books": page_obj.object_list,
                "page_obj": page_obj,
            },
        )

    elif request.method == "POST":
        qs = get_filtered_books(request.POST)

        paginator = Paginator(qs, 12)
        page_obj = paginator.get_page(request.GET.get("page"))

        return render(
            request,
            "books.html",
            {
                "books": page_obj.object_list,
                "page_obj": page_obj,
            },
        )

def books_search(request):
    search_query = request.GET.get("q", "")
    books = search_books(search_query)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "books.html", {"books": page_obj.object_list, "page_obj": page_obj, "search_query": search_query})

def book_page(request, slug):
    if request.method == "GET":
        data = get_book_page_data(request.user, slug)
        if not data:
            raise Http404("Book not found")
        return render(request, "book_page.html", data)
    
    elif request.method == "POST":
        if request.user.is_authenticated:
            message = request.POST.get("message")
            rate = request.POST.get("rating")
            
            _, data = process_book_comment(request.user, slug, message, rate)
            return render(request, "book_page.html", data)
        else:
            return redirect("/user/login/")

@login_required
@ratelimit(key='ip', rate='10/m')
def edit_comment(request):
    if request.method == "POST":
        method = request.POST.get("_method")
        if method == "get":
            book_slug = request.POST.get("book_slug")
            comment_id = request.POST.get("comment_id")
            data = get_edit_comment_data(request.user, book_slug, comment_id)
            return render(request, "book_page.html", data)
    
        elif method == "post":
            comment_id = request.POST.get("comment_id")
            message = request.POST.get("message")
            rate = request.POST.get("rating")
            book_slug = request.POST.get("book_slug")

            _, data = process_edit_comment(request.user, book_slug, comment_id, message, rate)
            return redirect(f"/books/book/{book_slug}")
    else :
        return redirect("/books/")

@login_required
@ratelimit(key='ip', rate='10/m')
def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        book_slug = request.POST.get("book_slug")
        process_delete_comment(request.user, comment_id)

        return redirect(f"/books/book/{book_slug}")

@login_required
@ratelimit(key='ip', rate='20/m')
def like_book(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        process_like_book(request.user, book_id)

        ref = request.META.get("HTTP_REFERER")
        if ref:
            path = urlparse(ref).path
            return redirect(path)
        return redirect("/")

@login_required
@ratelimit(key='ip', rate='20/m')
def unlike_book(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        process_unlike_book(request.user, book_id)

        ref = request.META.get("HTTP_REFERER")
        if ref:
            path = urlparse(ref).path
            return redirect(path)
        return redirect("/")
