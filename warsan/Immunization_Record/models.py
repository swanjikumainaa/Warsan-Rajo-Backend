from django.db import models
from vaccine.models import Vaccine
from child.models import Child
class Immunization_Record(models.Model): 
    child=models.OneToOneField(Child,on_delete=models.CASCADE,null=True)
    vaccine=models.ForeignKey(Vaccine,on_delete=models.CASCADE,null=True)
    date_of_administaration=models.DateTimeField(auto_now_add=True)
    next_date_of_administration= models.DateTimeField(auto_now=True)

    