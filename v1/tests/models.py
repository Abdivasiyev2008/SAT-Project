from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class Practice(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='practice/images/', blank=True, null=True)
    start_date = models.DateTimeField()
    action = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Practice obyektini saqlash

        # Agar action False bo'lsa va HidePractice da hali mavjud bo'lmasa, qo'shish
        if not self.action:
            HidePractice.objects.get_or_create(practice=self)


class HidePractice(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Practicedagi action False bo'lsa saqlash
        if self.practice.action:
            raise ValidationError("You can only link practices where action is False.")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.practice)  # Corrected to return a string representation of the practice


class HideUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user}")

class HideUserPractice(models.Model):
    user = models.ForeignKey(HideUser, on_delete=models.CASCADE)
    practice = models.ForeignKey(HidePractice, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user} -- {self.practice}")
