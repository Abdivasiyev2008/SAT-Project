from django.contrib import admin
from .models import *


class Module_2_QuestionInline(admin.TabularInline):
    model = Module_2_Question
    extra = 1  # Qo'shimcha bo'sh qator ko'rsatmaslik
    min_num = 1  # Kamida 1 qator
    can_delete = True  # Savollarni o'chirishga ruxsat berish


class Module_2_Admin(admin.ModelAdmin):
    inlines = [Module_2_QuestionInline]  # Module_2_Question modelini inline qilish


admin.site.register(Module_2, Module_2_Admin)
admin.site.register(Time2)
