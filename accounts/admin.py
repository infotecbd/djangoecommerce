from django.contrib import admin

from .models import CustomUser, ContactInfo, SocialLink, LegalPage

class SocialLinkInline(admin.StackedInline):
    model = SocialLink
    can_delete = False
    verbose_name_plural = 'Social Links'


class LegalPageInline(admin.StackedInline):
    model = LegalPage
    can_delete = False
    verbose_name_plural = 'Legal Pages'


class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline, LegalPageInline]

@admin.register(CustomUser, ContactInfo, SocialLink, LegalPage)

class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
