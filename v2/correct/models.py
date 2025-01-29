from django.db import models
from django.contrib.auth import get_user_model
from tests.models import Practice
import json
from ckeditor.fields import RichTextField

######################### Module 1 #########################

class Module1_Ans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.practice}"

    def save_answers(self, answers_dict):
        """Saves answers in JSON format"""
        self.answers = json.dumps(answers_dict)
        self.save()

class Answer1(models.Model):
    module1_ans = models.ForeignKey(Module1_Ans, on_delete=models.CASCADE)
    user_answer = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi
    correct_answer = RichTextField()  # Har doim to'g'ri javob saqlanadi
    question = RichTextField()


    def __str__(self):
        return f"Correct Answer: {self.correct_answer}"

######################### Module 2 #########################

class Module2_Ans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.practice}"

    def save_answers(self, answers_dict):
        """Saves answers in JSON format"""
        self.answers = json.dumps(answers_dict)
        self.save()

class Answer2(models.Model):
    module2_ans = models.ForeignKey(Module2_Ans, on_delete=models.CASCADE)
    user_answer = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi
    correct_answer = RichTextField()  # Har doim to'g'ri javob saqlanadi
    question = RichTextField()

    def __str__(self):
        return f"Correct Answer: {self.correct_answer}"



######################### Module 3 #########################

class Module3_Ans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.practice}"

    def save_answers(self, answers_dict):
        """Saves answers in JSON format"""
        self.answers = json.dumps(answers_dict)
        self.save()

class Answer3(models.Model):
    module3_ans = models.ForeignKey(Module3_Ans, on_delete=models.CASCADE)
    user_answer = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi
    correct_answer = RichTextField()  # Har doim to'g'ri javob saqlanadi
    question = RichTextField()

    def __str__(self):
        return f"Correct Answer: {self.correct_answer}"


######################### Module 4 #########################

class Module4_Ans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.practice}"

    def save_answers(self, answers_dict):
        """Saves answers in JSON format"""
        self.answers = json.dumps(answers_dict)
        self.save()

class Answer4(models.Model):
    module4_ans = models.ForeignKey(Module4_Ans, on_delete=models.CASCADE)
    user_answer = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi
    correct_answer = RichTextField()  # Har doim to'g'ri javob saqlanadi
    question = RichTextField()

    def __str__(self):
        return f"Correct Answer: {self.correct_answer}"


