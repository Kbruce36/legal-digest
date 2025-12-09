from django.contrib import admin

from .models import Case, Tag


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("title", "court", "decision_date", "status", "updated_at")
    list_filter = ("status", "court", "jurisdiction", "tags")
    search_fields = ("title", "citation", "court", "jurisdiction", "docket_number", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("tags",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
