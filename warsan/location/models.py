from django.db import models

# Create your models here.

class Location(models.Model):
    state = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    district = models.CharField(max_length=32)
    # vaccination_center = models.CharField(max_length=100)

    def __str__(self):
        return self.district