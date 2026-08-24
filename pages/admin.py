from django.contrib import admin
from .models import PageItem


@admin.register(PageItem)
class PageItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "short_description")

