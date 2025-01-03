from django.db import models

class Practice(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='practice/images/', blank=True, null=True)
    start_date = models.DateTimeField()

    def __str__(self):
        return self.name