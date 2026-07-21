from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta

from questions.models import Question
from library.models import Book

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    grade = models.CharField(null=True , blank=True)
    school_name = models.CharField(null=True , blank=True)
    score = models.FloatField(default=0 , null=False , db_index=True)
    profile_picture = models.IntegerField(default=1 , null=False)

    class Meta:
        indexes = [
            models.Index(fields=["-score"], name="userprofile_score_idx"),
        ]

    def __str__(self):
        return self.user.username    


class Badge(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(null=False , blank=False)
    description = models.CharField(null=False , blank=False)

    def __str__(self):
        return self.user.username

def four_hours_from_now():
    return timezone.now() + timedelta(hours=4)

class ForgotPassword(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    token = models.CharField(null=False , blank=False , db_index=True)
    expire_date = models.DateTimeField(default=four_hours_from_now)

    def __str__(self):
        return self.user.username
    

class Like(models.Model):
    liked_by = models.ForeignKey(User , on_delete=models.CASCADE , null=False)
    question = models.ForeignKey(Question , on_delete=models.CASCADE , null=True)
    book = models.ForeignKey(Book , on_delete=models.CASCADE , null=True)

    class Meta:
        indexes = [
            models.Index(fields=["liked_by", "question", "-id"], name="like_user_q_recent_idx"),
            models.Index(fields=["liked_by", "book", "-id"], name="like_user_b_recent_idx"),
        ]

    def __str__(self):
        return self.liked_by.username

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment_by = models.ForeignKey(User , on_delete=models.CASCADE , null=False)
    user_profile = models.ForeignKey(UserProfile , on_delete=models.CASCADE , null=False)
    question = models.ForeignKey(Question , on_delete=models.CASCADE , null=True)
    book = models.ForeignKey(Book , on_delete=models.CASCADE , null=True)
    message=models.CharField(null=False , blank=False , max_length=600)
    score=models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class DeleteAccount(models.Model):
    reason = models.TextField(null=True , blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.reason)[:20]