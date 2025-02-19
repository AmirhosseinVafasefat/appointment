from django.urls import path
from . import views

app_name = 'doctor'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_office', views.create_office, name='create_office'),
    path('edit_office', views.edit_office, name='edit_office'),
    path('add_appointments', views.add_appointments, name='add_appointments'),
    path('delete_appointment/<int:appointment_id>', views.delete_appointment, name='delete_appointment'),
]