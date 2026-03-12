from django.db import models

# Create your models here.
class CarouselImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="carousel/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title