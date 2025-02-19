from django.urls import path
from . import views

app_name = 'authuser'
urlpatterns = [
    path('login', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
    path('logout', views.logout_view, name='logout'),
    
]