from django.contrib import admin

from .models import PromoAdminModel


@admin.register(PromoAdminModel)
class PromoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "new_price", "old_price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description")