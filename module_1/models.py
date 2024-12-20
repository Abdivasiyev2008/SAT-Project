import re
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from tests.models import Practice


class Module_1(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Module: {self.practice}"

class Module_1_Question(models.Model):
    module = models.ForeignKey(Module_1, on_delete=models.CASCADE) 
    term = models.CharField(max_length=150)
    question = RichTextField()

    option_a = models.CharField(max_length=255, null=True, blank=True)
    option_b = models.CharField(max_length=255, null=True, blank=True)
    option_c = models.CharField(max_length=255, null=True, blank=True)
    option_d = models.CharField(max_length=255, null=True, blank=True)
    option_select_answer = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return f"Question for {self.term}"

