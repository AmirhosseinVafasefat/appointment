from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect(reverse('patient:index'))
    return render(request, 'authuser/login.html', {
        'form':form
    })

def registration_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.fields['phone_number']
            form.fields['username']= phone_number
            form.save()
            return HttpResponseRedirect(reverse('authuser:login'))
    return render(request, 'authuser/registration.html', {
        'form':form
    })

@login_required(login_url='/authuser/login')
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('authuser:login'))
    return render(request, 'authuser/logout.html')
