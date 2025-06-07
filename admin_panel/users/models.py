from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = "admin", _("Admin")
    USER = "user", _("User")
    RESTRICTED = "restricted", _("Restricted")


class UserState(models.TextChoices):
    ACTIVE = "active", _("Active")
    KICKED = "kicked", _("Kicked")
    BANNED = "banned", _("Banned")


class User(models.Model):
    class Meta:
        managed = False
        db_table = "users"

    id = models.AutoField(primary_key=True)
    tg_id = models.BigIntegerField(unique=True)
    user_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    langue_code = models.CharField(max_length=10)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    state = models.CharField(
        max_length=10,
        choices=UserState.choices,
        default=UserState.ACTIVE,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.tg_id})"
