from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True , auto_created=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-created_date"], name="chat_user_created_idx"),
        ]

class Message(models.Model):
    is_ai = models.BooleanField(null=False)
    text = models.TextField(null=False , blank=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="context" , null=True)

    class Meta:
        indexes = [
            models.Index(fields=["chat", "-id"], name="message_chat_recent_idx"),
        ]

class Memory(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    context = models.ManyToManyField(Message)