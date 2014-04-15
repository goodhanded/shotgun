from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse
from registration.forms import RegistrationForm
from drive.forms import RideForm, ProfileForm
from drive.models import Location, Ride, ShotgunProfile
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, "home.html", {
        'registrationForm':RegistrationForm(),
        'loginForm':AuthenticationForm(),
    })

def drive_logout(request):
    logout(request)
    return redirect('home')

def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=ShotgunProfile.objects.get(user=request.user))

        if form.is_valid():

            profile = form.save(commit=False)
            # profile.user = request.user
            profile.save()

            messages.success(request,'Your profile has been updated!')
            return redirect('home')

    else:
        #load current user into form
        user = request.user
    
        try:
            profile = getattr(user, 'shotgunprofile')
        except:
            profile = ShotgunProfile()
            profile.user = user
            profile.save()
        
        form = ProfileForm(instance=ShotgunProfile.objects.get(user=request.user))

    return render(request, 'profile/edit.html', {'form': form})

def profile_show(request, pk):
    user = get_object_or_404(User, id=pk)
    return render(request, "profile/show.html", {'user': user})

def rides_index(request):
    rides = Ride.objects.all()
    paginator = Paginator(rides, 10)
    page = request.GET.get('page')

    try:
        rides = paginator.page(page)
    except PageNotAnInteger:
        rides = paginator.page(1)
    except EmptyPage:
        rides = paginator.page(paginator.num_pages)

    return render(request, 'rides/index.html', {"rides": rides})

def rides_new(request):
    if request.method == 'POST':
        rideForm = RideForm(request.POST)

        if rideForm.is_valid():

            fromLoc = Location()
            fromLoc.lat = rideForm.cleaned_data['fromLat']
            fromLoc.lng = rideForm.cleaned_data['fromLng']
            fromLoc.formattedAddress = rideForm.cleaned_data['fromFormatted']
            fromLoc.city = rideForm.cleaned_data['fromLocality']
            fromLoc.save()

            toLoc = Location()
            toLoc.lat = rideForm.cleaned_data['toLat']
            toLoc.lng = rideForm.cleaned_data['toLng']
            toLoc.formattedAddress = rideForm.cleaned_data['toFormatted']
            toLoc.city = rideForm.cleaned_data['toLocality']
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

def rides_show(request, pk):
    ride = get_object_or_404(Ride, id=pk)
    return render(request, "rides/show.html", {'ride': ride})