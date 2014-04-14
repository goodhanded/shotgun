from django.db import models
from django.contrib.auth.models import User

class ShotgunProfile(models.Model):
    YEARS = (
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
        ('Professor', 'Professor'),
    )
    SCHOOLS = (
        ('UNC Chapel Hill', 'UNC Chapel Hill'),
    )
    PASSENGERS = (
        ('Males', 'Males'),
        ('Females', 'Females'),
        ('Males/Females', 'Males/Females'),
    )
    user = models.OneToOneField(User, related_name='shotgunprofile')
    avatar = models.ImageField(upload_to='images/avatars/', default='')
    school = models.CharField(max_length=50, choices=SCHOOLS, default='UNC Chapel Hill')
    year = models.CharField(max_length=10, choices=YEARS, default='Freshman')
    passengers = models.CharField(max_length=15, choices=PASSENGERS, default='Males/Females')

class Location(models.Model):
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    formattedAddress = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

class Ride(models.Model):
    driver = models.ForeignKey(User) 
    fromLocation = models.ForeignKey('Location', related_name='ride_from_set')
    toLocation = models.ForeignKey('Location', related_name='ride_to_set')
    leavingOn = models.DateField()
    gasMoney = models.DecimalField(max_digits=6, decimal_places=2)
    luggageRoom = models.IntegerField()
