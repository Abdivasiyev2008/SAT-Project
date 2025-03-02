from django.contrib import admin
from .models import Module_1, Module_1_Question, Time1


class Module_1_QuestionInline(admin.TabularInline):
    model = Module_1_Question
    extra = 1  # Qo'shimcha bo'sh qator ko'rsatmaslik
    min_num = 1  # Kamida 1 qator
    can_delete = True  # Savollarni o'chirishga ruxsat berish


class Module_1_Admin(admin.ModelAdmin):
    inlines = [Module_1_QuestionInline]  # Module_1_Question modelini inline qilish


admin.site.register(Module_1, Module_1_Admin)
admin.site.register(Time1)