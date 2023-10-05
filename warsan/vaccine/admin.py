from django.contrib import admin

from .models import Vaccine

class VaccineAdmin(admin.ModelAdmin):
    list_display = ("name", "target_disease", "minimum_age", "maximum_age", "recommended_dose", "date_created")
admin.site.register(Vaccine,VaccineAdmin)
