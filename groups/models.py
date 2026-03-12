from django.db import models
from django.conf import settings

# This module handles parish group data such as Choir, KCYM, CLC, etc.

class ParishGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    leader = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to="groups/logos/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
