from django.urls import path
from . import views

app_name = "patient"
urlpatterns = [
    path('', views.index, name='index'),
    path('office/<int:office_id>', views.office_view, name="office_view"),
    path('book_appointment/<int:appointment_id>', views.book_appointment, name="book_appointment"),
    path('cancel_appointment/<int:appointment_id>', views.cancel_appointment, name="cancel_appointment"),
    path('booked_appointments', views.booked_appointments, name="booked_appointments")
]