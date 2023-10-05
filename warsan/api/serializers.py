from rest_framework import serializers
from location.models import Location
from Immunization_Record.models import Immunization_Record
from vaccine.models import Vaccine
from child.models import Child, Guardian

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
from registration.models import CustomUser, Healthworker

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class HealthworkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Healthworker
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'location', 'created_by')

class Immunization_RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model =Immunization_Record
        fields='__all__'

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vaccine
        fields=("__all__")
    
class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = '__all__'
class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'