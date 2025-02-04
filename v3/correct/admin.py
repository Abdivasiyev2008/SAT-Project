from django.contrib import admin
from .models import *


class AnswerInline(admin.TabularInline):
    model = Answer2
    extra = 1  # Admin panelda bo'sh javob formalarini ko'rish uchun
    fields = ['user_answer', 'correct_answer']


@admin.register(Module2_Ans)
class Module1AnsAdmin(admin.ModelAdmin):
    list_display = ['user', 'practice']
    search_fields = ['user__username', 'practice__name']  # Foydalanuvchini yoki amaliyotni qidirish uchun
    inlines = [AnswerInline]  # Answer1 modeli inline tarzda ko'rsatiladi

