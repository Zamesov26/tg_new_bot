from django.db import models


class MediaType(models.TextChoices):
    PHOTO = "photo", "Photo"
    VIDEO = "video", "Video"
    DOCUMENT = "document", "Document"


class Media(models.Model):
    class Meta:
        managed = False
        db_table = "media"
    
    id = models.AutoField(primary_key=True)
    title  =  models.CharField(max_length=256)
    file_id = models.CharField(
        max_length=256, null=True, blank=True, unique=True
    )
    url = models.URLField(max_length=512, null=True, blank=True)
    file_path = models.CharField(max_length=512, null=True, blank=True)

    type = models.CharField(
        max_length=20, choices=MediaType.choices, default=MediaType.PHOTO
    )
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.caption or self.file_id or self.url or "Unnamed Media"
