from django.db import models
from tests.models import Practice
from django.contrib.auth import get_user_model

# Create your models here.

class Certificate(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    english = models.IntegerField(default=0)
    math = models.IntegerField(default=0)
    overall = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    module1 = models.BooleanField(default=False)
    
    module2 = models.BooleanField(default=False)
    
    module3 = models.BooleanField(default=False)    
    module4 = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} --- {self.practice}"


class Checking(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.practice} --- {self.user}"

