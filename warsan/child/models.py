
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from location.models import Location

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class Child(models.Model):
    first_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    guardian = models.ForeignKey('Guardian', on_delete=models.CASCADE, related_name='children')
   
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Child of {self.guardian})"



from django.db import models
from child.models import Child  

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    
)

class Guardian(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.ManyToManyField(Location)
    phone_number = PhoneNumberField(unique=True, region='IR')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def register_child(self):
        child = Child.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            guardian=self,
        )
        return child

    def get_children(self):
        return self.children.all()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"