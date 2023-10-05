
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from location.models import Location
from .serializers import LocationSerializer
from child.models import Child, Guardian
from .serializers import ChildSerializer, GuardianSerializer

class LocationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.location_data = {
            'state': 'Somaliland',
            'region': 'Awdal',
            'district': 'Baki',
        }
        self.location = Location.objects.create(**self.location_data)

    def test_list_locations(self):
        response = self.client.get('/api/location/') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_location(self):
        response = self.client.post('/api/location/', self.location_data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(Location.objects.last().state, 'Somaliland') 
        
    def test_get_location_detail(self):
        response = self.client.get(f'/api/location/{self.location.id}/')  
from django.urls import reverse
from Immunization_Record.models import Immunization_Record

class ImmunizationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('immunization_record_list_view')  
        self.detail_url = reverse('immunization_record_detail_view', args=[1])  

        self.immunization_record = Immunization_Record.objects.create(
            date_of_administaration="2023-09-05T06:00:00+00:00",
            next_date_of_administration="2023-09-06T18:00:00+00:00"
        )

    def test_get_immunization_record_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_immunization_record(self):
        data = {
          "date_of_administaration": "2023-09-05T06:00:00+00:00", 
         "next_date_of_administration": "2023-09-06T18:00:00+00:00" 
            
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_immunization_record_detail(self):
        response = self.client.get(self.detail_url)
        

    def test_update_immunization_record(self):
        data = {
             "date_of_administaration": "2023-08-08T06:00:00+00:00", 
             "next_date_of_administration": "2023-10-10T18:00:00+00:00" 
            
        }
        response = self.client.put(self.detail_url, data, format='json')
        
    def test_delete_immunization_record(self):
        response = self.client.delete(self.detail_url)
       
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vaccine.models import Vaccine
from .serializers import VaccineSerializer

class VaccineAPITestCase(APITestCase):

    def setUp(self):
        self.vaccine_data = {
            "name": "Hepetuitis C",
            "target_disease": "Hepetuitis",
            "minimum_age": 1,
            "maximum_age": 10,
            "recommended_dose": 1.5
        }
        self.vaccine = Vaccine.objects.create(**self.vaccine_data)

    def test_list_vaccines(self):
        url = reverse("vaccine_list_view")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vaccine(self):
        url = reverse("vaccine_list_view")
    
        # Validating the data using serializer
        serializer = VaccineSerializer(data=self.vaccine_data)
        if not serializer.is_valid():
         print(serializer.errors)  
    
        response = self.client.post(url, self.vaccine_data, format="json")
        print(response.content)

    def test_retrieve_vaccine(self):
        url = reverse("vaccine_detail_view", args=[self.vaccine.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vaccine(self):
        updated_data = {
            "name": "polio dose 2",
            "target_disease": "polio",
            "minimum_age": 2,
            "maximum_age": 12,
            "recommended_dose": 2.0
        }
        url = reverse("vaccine_detail_view", args=[self.vaccine.pk])
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)




def test_create_guardian(self):
    serialized_guardian = GuardianSerializer(data=self.guardian_data)
    if serialized_guardian.is_valid():
        serialized_guardian.save()
        response = self.client.post('/api/guardians/', self.guardian_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    else:
        self.fail(f"Guardian data is not valid: {serialized_guardian.errors}")
class ChildAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.child_data = {'first_name': 'Child 1', 'age': 5}
        self.child = Child.objects.create(first_name='Child 2', age=7)


