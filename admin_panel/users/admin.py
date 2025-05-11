from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("tg_id", "name", "state")
    list_filter = ("state",)
    search_fields = ("name", "tg_id")
