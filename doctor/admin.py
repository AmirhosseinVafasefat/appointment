from django.contrib import admin
from .models import City, Speciality, Office, Appointment

# Register your models here.
admin.site.register(City)
admin.site.register(Office)
admin.site.register(Appointment)
admin.site.register(Speciality)