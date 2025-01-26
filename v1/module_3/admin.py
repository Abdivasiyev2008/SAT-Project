from django.contrib import admin
from .models import Module_3, Module_3_Question


class Module_3_QuestionInline(admin.TabularInline):
    model = Module_3_Question
    extra = 1  # Qo'shimcha bo'sh qator ko'rsatmaslik
    min_num = 1  # Kamida 1 qator
    can_delete = True  # Savollarni o'chirishga ruxsat berish


class Module_3_Admin(admin.ModelAdmin):
    inlines = [Module_3_QuestionInline]  # Module_1_Question modelini inline qilish


admin.site.register(Module_3, Module_3_Admin)
