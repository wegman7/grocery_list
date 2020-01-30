from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class List(models.Model):
    item = models.CharField(max_length=200)
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.item