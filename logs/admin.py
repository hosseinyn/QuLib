from django.contrib import admin
from .models import UserAccessLog

# Register your models here.
@admin.register(UserAccessLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'os', 'path', 'ip', 'timestamp')
    readonly_fields = ('user', 'os', 'path', 'ip', 'timestamp')
    list_filter = ('user','os', 'timestamp')
    search_fields = ('user' , 'path')