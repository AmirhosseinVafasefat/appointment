from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from authuser.models import User
from doctor.models import Office, Appointment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    offices = Office.objects.all()
    return render(request, "patient/index.html", {
        'offices' : offices
    })

def office_view(request, office_id):
    office = Office.objects.get(pk=office_id)
    appointments = Appointment.objects.filter(office=office)
    days = set()
    for appointment in appointments:
        days.add(appointment.date)
    
    return render(request, "patient/office.html", {
        'days':days,
        'appointments':appointments
    })

@login_required(login_url='/authuser/login')
def book_appointment(request, appointment_id):
    if request.method == "POST":
        user = request.user
        appointment = Appointment.objects.get(pk=appointment_id)
        if appointment.is_available == True:    
            appointment.patient = user
            appointment.is_available = False
            appointment.save()
            return HttpResponseRedirect(reverse("patient:booked_appointments"))
    return HttpResponse("Not allowed!")

@login_required(login_url='/authuser/login')
def cancel_appointment(request, appointment_id):
    if request.method == "POST":
        user = request.user
        appointment = Appointment.objects.get(pk=appointment_id)
        if appointment.patient == user:    
            appointment.patient = None
            appointment.is_available = True
            appointment.save()
            return HttpResponseRedirect(reverse("patient:booked_appointments"))
    return HttpResponse("Not allowed!")

@login_required(login_url='/authuser/login')
def booked_appointments(request):
    user = request.user
    appointments = user.appointments.all()
    return render(request, "patient/booked.html", {
        'appointments':appointments
    })