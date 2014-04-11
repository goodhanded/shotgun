from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse
from registration.forms import RegistrationForm
from drive.forms import RideForm
from drive.models import Location, Ride
from django.contrib import messages
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
    if request.method == 'POST':
        rideForm = RideForm(request.POST)

        if rideForm.is_valid():

            fromLoc = Location()
            fromLoc.lat = rideForm.cleaned_data['fromLat']
            fromLoc.lng = rideForm.cleaned_data['fromLng']
            fromLoc.formattedAddress = rideForm.cleaned_data['fromFormatted']
            fromLoc.save()

            toLoc = Location()
            toLoc.lat = rideForm.cleaned_data['toLat']
            toLoc.lng = rideForm.cleaned_data['toLng']
            toLoc.formattedAddress = rideForm.cleaned_data['toFormatted']
            toLoc.save()

            ride = Ride()
            ride.driver = request.user
            ride.fromLocation = fromLoc
            ride.toLocation = toLoc
            ride.leavingOn = rideForm.cleaned_data['leavingOn']
            ride.gasMoney = rideForm.cleaned_data['gasMoney']
            ride.luggageRoom = rideForm.cleaned_data['luggageRoom']
            ride.save()

            messages.success(request,'Your ride has been posted!')
            return redirect('home')

    else:
        rideForm = RideForm()
    return render(request, 'rides/new.html', {'rideForm': rideForm})