from django import forms
from django.forms import ModelForm
from drive.models import ShotgunProfile

class RideForm(forms.Form):
    fromInput = forms.CharField(widget=forms.TextInput(attrs={'id':'address-from', 'class':'col-xs-12','autocomplete':'off'}), max_length=255)
    fromLat = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    fromLng = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    fromFormatted = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    fromLocality = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    toInput = forms.CharField(widget=forms.TextInput(attrs={'id':'address-to', 'class':'col-xs-12','autocomplete':'off'}), max_length=255)
    toLat = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    toLng = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    toFormatted = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    toLocality = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    leavingOn = forms.DateField(widget=forms.DateInput(attrs={'class':'col-xs-12','placeholder':'mm/dd/yyyy'}))
    gasMoney = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'col-xs-12', 'placeholder':'5.00'}), max_digits=6, decimal_places=2)
    luggageRoom = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'col-xs-12', 'placeholder':'5'}))

class ProfileForm(ModelForm):
    class Meta:
        model = ShotgunProfile
        fields = ['avatar','school','year','passengers']

class SearchForm(forms.Form):
    fromInput = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'address-from', 'class':'col-xs-12','autocomplete':'off'}), max_length=255)
    fromLat = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    fromLng = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    fromFormatted = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    fromLocality = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    toInput = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'address-to', 'class':'col-xs-12','autocomplete':'off'}), max_length=255)
    toLat = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    toLng = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    toFormatted = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    toLocality = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    leavingOn = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'col-xs-12','placeholder':'mm/dd/yyyy'}))
