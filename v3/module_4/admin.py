from django.contrib import admin
from .models import Module_4, Module_4_Question, Time4


class Module_4_QuestionInline(admin.TabularInline):
    model = Module_4_Question
    extra = 1  # Qo'shimcha bo'sh qator ko'rsatmaslik
    min_num = 1  # Kamida 1 qator
    can_delete = True  # Savollarni o'chirishga ruxsat berish


class Module_4_Admin(admin.ModelAdmin):
    inlines = [Module_4_QuestionInline]  # Module_1_Question modelini inline qilish


admin.site.register(Module_4, Module_4_Admin)
