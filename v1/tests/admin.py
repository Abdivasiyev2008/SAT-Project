from django.contrib import admin
from .models import Practice, HidePractice, HideUserPractice, HideUser
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name', 'action')
    search_fields = ('name',)



class HideUserPracticeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue

            if form.cleaned_data.get('practice') and not form.cleaned_data['practice'].practice.action:
                raise ValidationError("You can only link practices where action is True.")


class HideUserPracticeInline(admin.TabularInline):
    model = HideUserPractice

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "practice":
            # Faqat Practice.action=False bo'lgan HidePractice obyektlarini ko'rsatish
            kwargs["queryset"] = HidePractice.objects.filter(practice__action=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HideUser)
class HideUserAdmin(admin.ModelAdmin):
    inlines = [HideUserPracticeInline]
    search_fields = ('user__user', 'hideuserpractice__practice__practice__name')