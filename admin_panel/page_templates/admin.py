from django.contrib import admin

from .models import TemplateAdminModel


@admin.register(TemplateAdminModel)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "model", "list_image_path")
    list_filter = ("type",)
    search_fields = ("model", "list_template", "item_template")
    readonly_fields = ("id",)
    
    fieldsets = (
        (None, {
            "fields": ("id", "type", "model")
        }),
        ("Templates", {
            "fields": ("list_template", "item_template")
        }),
        ("Images", {
            "fields": ("list_image_path",),
            "classes": ("collapse",)
        }),
    )
