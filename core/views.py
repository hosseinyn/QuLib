from django.shortcuts import render

from .forms import ContactForm

from .services.core_service import process_contact_form, get_leaderboard_users
from django_ratelimit.decorators import ratelimit
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request):
    return render(request , 'index.html')

def about(request):
    return render(request , 'about.html')

def partnership(request):
    return render(request , 'partnership.html')

@ratelimit(key='ip', rate='5/m')
def contact(request: HttpRequest) -> HttpResponse:
    """
    Handle contact form submission with rate limiting.
    """
    if request.method == "GET" :
        form = ContactForm
        return render(request , 'contact.html' , {"form" : form})
    if request.method == "POST": 
        form = ContactForm(request.POST)
        if form.is_valid():
            process_contact_form(form.cleaned_data)
            form = ContactForm
            return render(request , 'contact.html' , {"form" : form , "state" : "success"})
        else :
            form = ContactForm 
            return render(request , 'contact.html' , {"form" : form , "state" : "fail"})
        

def faq(request):
     return render(request , 'faq.html')

def reviews(request):
     return render(request , 'reviews.html')


def leaderboard(request):

    top_users = get_leaderboard_users()

    return render(request , "leaderboard.html" , {"top_users" : top_users})

def terms(request):
    return render(request , "terms.html")

def privacy(request):
    return render(request , "privacy.html")


def custom_403(request , exception=None):
    return render(request, "403.html", status=403)

def custom_404(request , exception=None):
    return render(request, "404.html", status=404)
