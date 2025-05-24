from django.contrib import admin

from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "file_id",
        "url",
        "file_path",
        "short_caption",
    )
    search_fields = ("file_id", "url", "caption")
    list_filter = ("type",)

    def short_caption(self, obj):
        return (
            (obj.caption[:30] + "...")
            if obj.caption and len(obj.caption) > 30
            else obj.caption
        )

    short_caption.short_description = "Caption"
