from django.db import models
from django.utils import timezone

# Create your models here.

class LeakPassword(models.Model):
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-time']  # Orders by 'time' in descending order

    def __str__(self):
        # Handle None values by using an empty string if a field is None
        url = self.url if self.url else ""
        username = self.username if self.username else ""
        password = self.password if self.password else ""
        return f"{url} | {username} | {password}"
