from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Authentication identity only. Roles live on actor profile models."""

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
