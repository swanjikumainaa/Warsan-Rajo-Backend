
from django.db import models

class Vaccine(models.Model):

    name=models.CharField(max_length=32, unique= True)
    target_disease = models.CharField(max_length=32)
    minimum_age = models.IntegerField()
    maximum_age =models.IntegerField()
    recommended_dose = models.DecimalField(max_digits=6, decimal_places=3)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):          
        return self.name



