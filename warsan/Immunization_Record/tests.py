
from django.test import TestCase
from .models import Immunization_Record
from django.utils import timezone

class ImmunizationRecordTestCase(TestCase):
    def setUp(self):
        self.immunization_record = Immunization_Record.objects.create()

    def test_date_of_administration(self):
        now = timezone.now()
        self.assertLess(self.immunization_record.date_of_administaration, now)

    def test_next_date_of_administration(self):
        now = timezone.now()
        self.assertLess(self.immunization_record.next_date_of_administration, now)

