from django.contrib import admin

from .models import UserProfile , Comment , Badge , DeleteAccount

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['grade', 'school_name' , 'score']
    list_filter = ['grade']
    search_fields = ['school_name']
admin.site.register(Comment)
admin.site.register(Badge)
@admin.register(DeleteAccount)
class DeleteAccountAdmin(admin.ModelAdmin):
    list_display = ['reason', 'date']
    list_filter = ['date']
    search_fields = ['reason']
