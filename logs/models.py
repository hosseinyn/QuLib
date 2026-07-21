from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    os = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.user:
            return self.user.username
        else :
            return "ناشناس"