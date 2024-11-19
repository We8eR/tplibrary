from django.db import models
from django.utils import timezone

class AddTP(models.Model):
    author = models.CharField(max_length=200, null=False, blank=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title