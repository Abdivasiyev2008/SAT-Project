import re, datetime
import matplotlib
import matplotlib.pyplot as plt
import pylab
from PIL import Image
from io import BytesIO
from django.db import models
from ckeditor.fields import RichTextField
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
from tests.models import Practice

matplotlib.use('Agg')  # GUI ni o'chirib qo'yish
matplotlib.rcParams['text.usetex'] = False  # LaTeXni ishlatmaslik (oddiy matnlar uchun)

class Module_4(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Module: {self.practice}"

class Module_4_Question(models.Model):
    module = models.ForeignKey(Module_4, on_delete=models.CASCADE) 
    term = models.CharField(max_length=2000, null=True, blank=True)
    question = RichTextField(null=True, blank=True)

    option_a = models.CharField(max_length=2000, null=True, blank=True)
    option_b = models.CharField(max_length=2000, null=True, blank=True)
    option_c = models.CharField(max_length=2000, null=True, blank=True)
    option_d = models.CharField(max_length=2000, null=True, blank=True)
    image = models.ImageField(upload_to='question/images/', null=True, blank=True)
    option_select_answer = models.CharField(max_length=1, null=True, blank=True)
    option_input_answer = models.CharField(max_length=2000, null=True, blank=True)
    explanation = RichTextField(null=True, blank=True)  # Har doim to'g'ri javob saqlanadi

    def __str__(self):
        return f"Question for {self.term}"

    def save(self, *args, **kwargs):
        # Rasmni yaratish va saqlash
        if not self.image and self.question:  # image bo'sh va question mavjud bo'lsa
            try:
                # Matnni rasmga aylantirish (LaTeX ishlatmasdan)
                img = self.generate_text_image(self.clean_html(self.question))
    
                image_buffer = BytesIO()
                img.save(image_buffer, format='PNG')
                image_buffer.seek(0)
    
                safe_filename = self.sanitize_filename(self.term)  # Fayl nomini term bo'yicha yaratish
    
                # Rasmni ContentFile orqali saqlash
                self.image.save(f"{safe_filename}.png", ContentFile(image_buffer.read()), save=False)
    
            except Exception as e:
                print(f"Xatolik rasm yaratishda: {e}")
    
        super().save(*args, **kwargs)

    def clean_html(self, text):
        """
        HTML teglarini olib tashlash va faqat matnni olish.
        """
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()  # HTML teglarini olib tashlaydi va faqat matnni qaytaradi

    def generate_text_image(self, text):
        """
        Oddiy matnni rasmga aylantirish.
        """
        fig = plt.figure(figsize=(6, 1))  # Kengligi 6 dyuym, bo'yi 1 dyuym (matnni ko'rsatish uchun)
        
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, text, fontsize=14, ha='center', va='center')  # Oddiy matnni markazlashtirish

        # O'q chizish va boshqa elementlarni olib tashlash
        ax.axis('off')

        # Rasmni yaratish
        dpi = 100  # Rasmni 100 dpi bilan saqlash
        image_buffer = BytesIO()
        fig.savefig(image_buffer, format='PNG', dpi=dpi)
        image_buffer.seek(0)

        img = Image.open(image_buffer)
        img = img.resize((600, 100))  # Rasmni 600x100 o'lchamiga o'zgartirish (matnni ko'rsatish uchun)
        return img

    def sanitize_filename(self, text):
        """
        Fayl nomini xavfsiz qilish.
        """
        sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', text)  # Maxsus belgilarni olib tashlash
        sanitized = sanitized.replace(" ", "_")  # Bo'sh joylarni pastki chiziq bilan almashtirish
        return sanitized



class Time4(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    time = models.IntegerField(default=35 * 60)  # Default 35 daqiqa soniyada
    updated_at = models.DateTimeField(auto_now=True)  # So'nggi yangilanish vaqti

    def save(self, *args, **kwargs):
        # Vaqt yangilanishini tekshirish
        if self.pk:  # Agar obyekt avvaldan mavjud bo'lsa
            original_time = Time4.objects.get(pk=self.pk).time
            if self.time != original_time:
                self.updated_at = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.practice} - {self.time} seconds"
