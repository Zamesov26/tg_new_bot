from django.db import models


class TemplateType(models.TextChoices):
    PAGE = "PAGE", "PAGE"
    PAGINATE = "PAGINATE", "PAGINATE"
    # TODO можно подумать о других типах шаблонов


class TemplateAdminModel(models.Model):
    class Meta:
        db_table = "templates"
        managed = False
        unique_together = ("type", "model")
    
    id = models.IntegerField(primary_key=True)
    type = models.CharField(
        max_length=16,
        choices=TemplateType.choices,
    )
    model = models.CharField(max_length=128)
    list_template = models.TextField()
    list_image_path = models.CharField(max_length=256, null=True, blank=True)
    item_template = models.TextField(null=True, blank=True)
    
