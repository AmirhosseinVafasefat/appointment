from django.contrib import admin
from .models import City, Speciality, Office, Appointment, Notification

# Register your models here.
admin.site.register(City)
admin.site.register(Office)
admin.site.register(Appointment)
admin.site.register(Speciality)
admin.site.register(Notification)