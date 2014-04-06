from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def home(request):
    return render(request, "home.html", {
        'registrationForm':RegistrationForm(),
        'loginForm':AuthenticationForm(),
    })


def drive_logout(request):
    logout(request)
    return redirect('home')

def rides_new(request):
    return render(request, 'rides/new.html')