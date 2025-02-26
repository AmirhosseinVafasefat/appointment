from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from authuser.models import User
from django.contrib.auth.decorators import login_required

from doctor.models import Office, Appointment, Notification


def cal_num_unread_notifications(user):
    if not Notification.objects.filter(recipient=user).exists():
        return 0
    else:
        return Notification.objects.filter(recipient=user, unread=True).count()
    
# Create your views here.
def index(request):
    offices = Office.objects.all()
    num_unread_notifications = cal_num_unread_notifications(request.user)

    return render(request, "patient/index.html", {
        'offices' : offices,
        'num_unread_notifications' : num_unread_notifications
    })

def office_view(request, office_id):
    office = Office.objects.get(pk=office_id)
    appointments = Appointment.objects.filter(office=office).order_by('date', 'time')
    days = set()
    for appointment in appointments:
        days.add(appointment.date)
    
    num_unread_notifications = cal_num_unread_notifications(request.user)

    return render(request, "patient/office.html", {
        'days':days,
        'appointments':appointments,
        'num_unread_notifications': num_unread_notifications
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

    num_unread_notifications = cal_num_unread_notifications(request.user)

    return render(request, "patient/booked.html", {
        'appointments':appointments,
        'num_unread_notifications': num_unread_notifications
    })

@login_required(login_url='/authuser/login')
def notifications_view(request):
    user = request.user
    if Notification.objects.filter(recipient=user).exists():
        notifications = Notification.objects.filter(recipient=user).all().order_by('-date', 'time')
    else:
        notifications = []
    
    for notification in notifications:
        notification.unread = False
        notification.save()

    num_unread_notifications = cal_num_unread_notifications(request.user)

    return render(request, 'patient/notifications.html', {
        'notifications': notifications,
        'num_unread_notifications': num_unread_notifications
    })
