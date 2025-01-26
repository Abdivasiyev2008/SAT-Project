import re
from django.db import models
from ckeditor.fields import RichTextField
from tests.models import Practice


class Module_2(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Module: {self.practice}"

class Module_2_Question(models.Model):
    module = models.ForeignKey(Module_2, on_delete=models.CASCADE)  # Reference to Module_2
    term = models.CharField(max_length=150)
    question = RichTextField()

    option_a = models.CharField(max_length=255, null=True, blank=True)
    option_b = models.CharField(max_length=255, null=True, blank=True)
    option_c = models.CharField(max_length=255, null=True, blank=True)
    option_d = models.CharField(max_length=255, null=True, blank=True)
    option_select_answer = models.CharField(max_length=1, null=True, blank=True)
    option_input_answer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Question for {self.term}"
