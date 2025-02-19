from django import forms
from django.forms.models import ModelForm
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from .models import City, Office, Speciality

class CreateOffice(ModelForm):
    speciality = forms.ModelChoiceField(label='تخصص',
                                        queryset=Speciality.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                    'required': 'true'}))
    image = forms.ImageField(label='عکس',
                             required=False)
    
    city = forms.ModelChoiceField(label='شهر',
                                queryset=City.objects.all(),
                                required=True,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    
    address = forms.CharField(label='آدرس',
                              required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    telephone_number = forms.CharField(label='شماره تلفن',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'required': 'true'}))
    class Meta:
        model = Office
        fields = ['speciality',  'city', 'address', 'telephone_number', 'image']


INTERVALS = [("5", "5"),
             ("10", "10"),
             ("15", "15"),
             ("20", "20"),
             ("30", "30"),
             ("40", "40"),
             ("60", "60")]

class AddAppointmentForm(forms.Form):
    date = JalaliDateField(label=('تاریخ'), # date format is  "yyyy-mm-dd"
            widget=AdminJalaliDateWidget # optional, to use default datepicker
        )
    starting_time = forms.TimeField(label='زمان شروع')
    ending_time = forms.TimeField(label='زمان شروع')
    interval = forms.ChoiceField(label='فاصله بین نوبت‌ها', choices=INTERVALS)