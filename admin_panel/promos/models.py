from django.db import models


class PromoAdminModel(models.Model):
    class Meta:
        managed = False
        db_table = "promo"
        verbose_name = "Акция"
        verbose_name_plural = "Акциии"

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField(blank=True, null=True)
    
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
