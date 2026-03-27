from django.contrib import admin
from .models import ContentItem


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "title", "last_updated")
    search_fields = ("source", "title")
