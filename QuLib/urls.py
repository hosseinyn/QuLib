"""
URL configuration for QuLib project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.contrib.sitemaps.views import sitemap

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from news.api import api as news_api
from news.views import subscriber_leave
from questions.api import api as questions_api
from .sitemaps import QuestionSitemap, BookSitemap

sitemaps = {
    'questions': QuestionSitemap,
    'books': BookSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('core.urls')),
    path('questions/api/', questions_api.urls),
    path('news/api/', news_api.urls),
    path('news/api/leave/<str:subscriber_uuid>' , view=subscriber_leave),
    path('user/' , include('user.urls')),
    path('questions/' , include('questions.urls')),
    path('books/' , include("library.urls")),
    path('qulib-ai/' , include('ai.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
            "llms.txt",
            TemplateView.as_view(template_name="llms.txt", content_type="text/plain"),
        ),

    path('' , include("pwa.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = "core.views.custom_403"
handler404 = "core.views.custom_404"
