from django.contrib import admin

from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ()
