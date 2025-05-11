from django.db import models
from django.utils.translation import gettext_lazy as _


class UserState(models.TextChoices):
    ACTIVE = "active", _("Active")
    KICKED = "kicked", _("Kicked")
    BANNED = "banned", _("Banned")


class User(models.Model):
    class Meta:
        managed = False
        db_table = "users"

    tg_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=10)
    state = models.CharField(max_length=10, choices=UserState.choices)

    def __str__(self):
        return f"{self.name} ({self.tg_id})"
