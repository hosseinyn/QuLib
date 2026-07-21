from django.db import models
import uuid

# Create your models here.
class Subscriber(models.Model):
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

class News(models.Model):
    subject = models.CharField(blank=False , null=False)
    message = models.TextField(blank=False , null=False)
    sent = models.DateField(auto_now_add=True)

    def __str__(self): 
        return self.subject