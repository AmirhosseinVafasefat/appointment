from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("شماره تلفن درست را وارد کنید.")
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, phone_number = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(phone_number, password, **extra_fields)
    
    def create_superuser(self, phone_number = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self._create_user(phone_number, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, blank=True, default='', validators=[RegexValidator(r'^09[0-9]{9}$')])
    name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')


    is_specialist = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    signup_date = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    
    REQUIRED_FIELDS = []
    
    class Meta():
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_short_name(self):
        return self.name
    
    def get_full_name(self):
        return self.name + self.last_name