from django.db import models
from django.conf import settings
from datetime import date
from groups.models import ParishGroup

User = settings.AUTH_USER_MODEL


class FamilyUnit(models.Model):
    """Each parish has multiple family units (wards)"""
    name = models.CharField(max_length=100, unique=True)
    president = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="unit_president"
    )

    logo = models.ImageField(
        upload_to="units/logos/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Family(models.Model):
    house_name = models.CharField(max_length=100, help_text="Ex: Mathew Bhavan")
    address = models.TextField(blank=True, null=True, help_text="Full postal address")
    family_photo = models.ImageField(upload_to="families/photos/", blank=True, null=True)
    family_register = models.ImageField(upload_to="families/registers/", blank=True, null=True)

    family_unit = models.ForeignKey(
        FamilyUnit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="families"
    )

    family_head = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_family"
    )

    def __str__(self):
        return self.house_name




class FamilyMember(models.Model):
    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name="members"
    )

    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="family_members/", blank=True, null=True)
    dob = models.DateField("Date of Birth", null=True, blank=True)

    parish_groups = models.ManyToManyField(
        ParishGroup,
        blank=True,
        related_name="members"
    )

    is_family_head = models.BooleanField(default=False)

    @property
    def age(self):
        if self.dob:
            from datetime import date
            today = date.today()
            return today.year - self.dob.year - (
                (today.month, today.day) < (self.dob.month, self.dob.day)
            )
        return None

    def __str__(self):
        return f"{self.name} ({self.family.house_name})"