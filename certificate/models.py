from django.db import models
from tests.models import Practice
from django.contrib.auth import get_user_model

# Create your models here.

class Certificate(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    english = models.IntegerField()
    math = models.IntegerField()
    overall = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} + {self.practice}"


class Checking(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
