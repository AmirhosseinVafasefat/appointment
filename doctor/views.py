from django.shortcuts import render, HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.urls import reverse
import datetime as dt
from django.contrib.auth.decorators import login_required, user_passes_test

from .decorators import specialist_check
from .models import City, Speciality, Office, Appointment, Notification
from .forms import CreateOffice, AddAppointmentForm

# Create your views here.
@login_required(login_url='/authuser/login')
@specialist_check
def index(request):
    user = request.user
    office = user.office.get()
    #TODO write clean and optimized code 
    try:
        appointments = Appointment.objects.filter(office=office).order_by('date', 'time')
        days = set()
        for appointment in appointments:
            days.add(appointment.date)
    except (Office.DoesNotExist, Appointment.DoesNotExist):
        appointments = None
        days = None
    return render(request, 'doctor/index.html', {
        'days': days,
        'appointments': appointments
    })

@login_required(login_url='/authuser/login')
@specialist_check
def create_office(request):
    form = CreateOffice()
    user = request.user
    if Office.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('doctor:edit_office'))
    
    if request.method == "POST":
        form = CreateOffice(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return HttpResponseRedirect(reverse('doctor:index'))

    return render(request, 'doctor/create_office.html', {
        'form': form
    })

@login_required(login_url='/authuser/login')
@specialist_check
def edit_office(request):
    user = request.user
    if not Office.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('doctor:create_office'))
    
    office = Office.objects.get(user=user)
    form = CreateOffice(instance=office)
    
    if request.method == "POST":
        form = CreateOffice(request.POST, request.FILES, instance=office)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('doctor:index'))

    return render(request, 'doctor/edit_office.html', {
        'form': form
    })

@login_required(login_url='/authuser/login')
@specialist_check
def add_appointments(request):
    user = request.user
    message = str()
    if not Office.objects.filter(user=user).exists():
        return HttpResponseRedirect(reverse('doctor:create_office'))
    
    form = AddAppointmentForm()
    if request.method == "POST":
        form = AddAppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            starting_time = form.cleaned_data["starting_time"]
            ending_time = form.cleaned_data["ending_time"]
            interval = form.cleaned_data["interval"]
            interval = dt.timedelta(minutes=int(interval))

            office = user.office.get()
            if not Appointment.objects.filter(office=office).exists():
                previous_appointments = []
            else:
                previous_appointments = office.appointments.all()

            appointment_time = starting_time
            while appointment_time < ending_time:

                appointment = Appointment(office=office, date=date, time=appointment_time, is_available=True)
                if not Appointment.objects.filter(date=date, time=appointment_time).exists():
                    appointment.save()

                appointment_time = (dt.datetime.combine(dt.date(1,1,1),appointment_time) + interval).time()

            if not Appointment.objects.filter(office=office).exists():
                appointments = []
            else:
                appointments = office.appointments.all()

            if appointments == previous_appointments:
                message = 'با موفقیت ذخیره شد.'
            elif appointments == []:
                message = 'نوبتی ذخیره نشد.'
            else:
                message = 'نوبت‌ها تکراری بودند.'
                                  
    return render(request, 'doctor/add_appointments.html', {
        'message': message,
        'form':form
    })

@login_required(login_url='/authuser/login')
@specialist_check   
def delete_appointment(request, appointment_id):
    if request.method == "POST":
        user = request.user
        office = user.office.get()
        appointment = Appointment.objects.filter(pk=appointment_id).get()
        if appointment.office == office:
            appointment.delete()
        return HttpResponseRedirect(reverse('doctor:index'))

@login_required(login_url='/authuser/login')
@specialist_check
def cancel_appointment(request, appointment_id):
    if request.method == "POST":
        user = request.user
        office = user.office.get()
        appointment = Appointment.objects.filter(pk=appointment_id).get()
        patient = appointment.patient

        if appointment.office == office:
            message = f"نوبت {appointment.date} {appointment.time}، مطب {appointment.office} از سوی متخصص لغو شد."
            time = dt.datetime.now().time()
            date = dt.datetime.now().date()
            cancelation =  Notification(message=message, sender=user, recipient=patient, date=date, time=time)
            cancelation.save()
            appointment.patient = None
            appointment.is_available = True
            appointment.save()

        return HttpResponseRedirect(reverse('doctor:index'))