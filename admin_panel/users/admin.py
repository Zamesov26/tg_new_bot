from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "tg_id",
        "user_name",
        "first_name",
        "last_name",
        "langue_code",
        "role",
        "state",
    )
    list_filter = ("role", "state")
    search_fields = ("tg_id", "user_name", "first_name", "last_name")
