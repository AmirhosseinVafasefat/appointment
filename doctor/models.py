from django.db import models
from authuser.models import User

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=30, blank=False)
    province = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.name + " || " + self.province    

class Speciality(models.Model):
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name


class Office(models.Model):
    user = models.ForeignKey(User, blank= False, related_name='office', on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, blank= False, related_name='offices', on_delete=models.DO_NOTHING)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    city = models.ForeignKey(City, blank=False, related_name='offices', on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255, blank=False)
    telephone_number = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return self.user.name + " " + self.user.last_name + " || " + Speciality.__str__(self.speciality) + " in " + City.__str__(self.city)

class Appointment(models.Model):
    patient = models.ForeignKey(User, null=True, blank=True, related_name='appointments', on_delete=models.DO_NOTHING)
    office = models.ForeignKey(Office, blank=False, related_name='appointments', on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return Office.__str__(self.office) + " " + str(self.date) + " " + str(self.is_available)