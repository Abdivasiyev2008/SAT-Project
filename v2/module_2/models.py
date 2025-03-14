import re
from django.db import models
from ckeditor.fields import RichTextField
from tests.models import Practice
from django.contrib.auth import get_user_model
import datetime


class Module_2(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Module: {self.practice}"

class Module_2_Question(models.Model):
    module = models.ForeignKey(Module_2, on_delete=models.CASCADE)  # Reference to Module_2
    term = models.CharField(max_length=2000)
    question = RichTextField()
    image = models.ImageField(upload_to="module2/images/", null=True, blank=True)

    option_a = models.CharField(max_length=2000, null=True, blank=True)
    option_b = models.CharField(max_length=2000, null=True, blank=True)
    option_c = models.CharField(max_length=2000, null=True, blank=True)
    option_d = models.CharField(max_length=2000, null=True, blank=True)
    option_select_answer = models.CharField(max_length=1, null=True, blank=True)
    explanation = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi

    def __str__(self):
        return f"Question for {self.term}"

class Time2(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    time = models.IntegerField(default=32 * 60)  # Default 32 daqiqa soniyada
    updated_at = models.DateTimeField(auto_now=True)  # So'nggi yangilanish vaqti

    def save(self, *args, **kwargs):
        # Vaqt yangilanishini tekshirish
        if self.pk:  # Agar obyekt avvaldan mavjud bo'lsa
            original_time = Time2.objects.get(pk=self.pk).time
            if self.time != original_time:
                self.updated_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.practice} - {self.time} seconds"
