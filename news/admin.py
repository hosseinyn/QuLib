from django.contrib import admin

from .models import Subscriber , News

# Register your models here.
admin.site.register(Subscriber)
admin.site.register(News)