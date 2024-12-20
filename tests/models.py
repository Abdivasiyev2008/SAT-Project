from django.db import models
from django.contrib.auth import get_user_model

class Practice(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='practice/images/', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name