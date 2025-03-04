from django.db import models

# Create your models here.

class TelegramChannel(models.Model):
    url = models.CharField(max_length=250)
    password = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.url
    
    