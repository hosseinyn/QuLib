from celery import shared_task
from .models import UserAccessLog
from django.contrib.auth.models import User

@shared_task
def submit_log_to_db(user , path , os , ip):
    if user :
        user = User.objects.filter(id=user).first()
    UserAccessLog.objects.create(
            user=user,
            os=os,
            path=path,
            ip=ip,
    )