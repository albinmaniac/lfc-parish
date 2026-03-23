from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True
    )

    date = models.DateField()

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True   # ✅ ADD THIS (important)
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True   # ✅ ADD THIS (admin panel safety)
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["date"]   # ✅ cleaner than repeating in views

    def __str__(self):
        return self.title