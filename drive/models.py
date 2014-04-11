from django.db import models
from django.contrib.auth.models import User

class ShotgunProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='images/sports/', blank=True, default='')

class Location(models.Model):
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    formattedAddress = models.CharField(max_length=255)

class Ride(models.Model):
    driver = models.ForeignKey(User) 
    fromLocation = models.ForeignKey('Location', related_name='ride_from_set')
    toLocation = models.ForeignKey('Location', related_name='ride_to_set')
    leavingOn = models.DateField()
    gasMoney = models.DecimalField(max_digits=6, decimal_places=2)
    luggageRoom = models.IntegerField()
