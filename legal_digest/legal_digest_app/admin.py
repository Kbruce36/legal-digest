from django.contrib import admin

from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ("title", "court", "decision_date", "status", "updated_at")
    list_filter = ("status", "court", "jurisdiction")
    search_fields = ("title", "citation", "court", "jurisdiction", "docket_number")
    prepopulated_fields = {"slug": ("title",)}
