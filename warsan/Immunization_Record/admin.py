from django.contrib import admin
from .models import Immunization_Record
class ImmunizationAdmin(admin.ModelAdmin):
    list_display= ("child","vaccine","date_of_administaration","next_date_of_administration")
admin.site.register(Immunization_Record,ImmunizationAdmin)   


