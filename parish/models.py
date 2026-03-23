from django.db import models
from django.conf import settings

class GalleryImage(models.Model):
    title = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to="gallery/")
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title




class Parish(models.Model):
    name = models.CharField(max_length=200)

    about = models.TextField(blank=True)

    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    mass_timings = models.TextField(
        blank=True,
        help_text="Example: Sunday 7:00 AM & 9:30 AM | Weekdays 6:30 AM"
    )

    logo = models.ImageField(
        upload_to="parish/",
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class ParishLeader(models.Model):
    ROLE_CHOICES = [
        ("vicar", "Vicar (വികാരി)"),
        ("kaikaran", "Kaikaran (കൈക്കാരൻ)"),
        ("secretary", "Secretary (സെക്രട്ടറി)"),
        ("church_servant", "Church Servant (ദേവാലയ ശുശ്രൂഷി)"),

        # ✅ NEW ROLES
        ("provincial", "Provincial (പ്രൊവിൻഷ്യൽ)"),
        ("vice_chairman", "Vice Chairman (വൈസ് ചെയർമാൻ)"),
    ]

    parish = models.ForeignKey(
        Parish,
        on_delete=models.CASCADE,
        related_name="leaders"
    )

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="parish/leaders/", blank=True, null=True)

    term_start = models.DateField()
    term_end = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_role_display()} - {self.name}"