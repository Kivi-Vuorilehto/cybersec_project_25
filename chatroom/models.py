from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    time = models.DateTimeField(default=timezone.now)
