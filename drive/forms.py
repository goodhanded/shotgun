from django import forms
from django.forms import ModelForm
from drive.models import ShotgunProfile
from haystack.forms import SearchForm

class RideForm(forms.Form):
    fromInput = forms.CharField(widget=forms.TextInput(attrs={'id':'address-from', 'class':'col-md-12','autocomplete':'off'}), max_length=255)
    fromLat = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    fromLng = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    fromFormatted = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    fromLocality = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    toInput = forms.CharField(widget=forms.TextInput(attrs={'id':'address-to', 'class':'col-md-12','autocomplete':'off'}), max_length=255)
    toLat = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    toLng = forms.DecimalField(widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    toFormatted = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    toLocality = forms.CharField(widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    leavingOn = forms.DateField(widget=forms.DateInput(attrs={'class':'col-md-12'}))
    gasMoney = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'col-md-12'}), max_digits=6, decimal_places=2)
    luggageRoom = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'col-md-12'}))

class ProfileForm(ModelForm):
    class Meta:
        model = ShotgunProfile
        fields = ['avatar','school','year','passengers']

class RideSearchForm(SearchForm):
    fromInput = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'address-from', 'class':'col-md-12','autocomplete':'off'}), max_length=255)
    fromLat = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    fromLng = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    fromFormatted = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    fromLocality = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    toInput = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'address-to', 'class':'col-md-12','autocomplete':'off'}), max_length=255)
    toLat = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lat'}), max_digits=20, decimal_places=16)
    toLng = forms.DecimalField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'lng'}), max_digits=20, decimal_places=16)
    toFormatted = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'formatted_address'}), max_length=255)
    toLocality = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'data-geo':'locality'}), max_length=255)

    leavingOn = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'col-md-12'}))

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(RideSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['fromLat'] and self.cleaned_data['fromLng']:
            fromPoint = Point(self.cleaned_data['fromLat'], self.cleaned_data['fromLng'])
            sqs = sqs.dwithin('fromLocation', fromPoint, 50)
        else:
            fromPoint = None

        if self.cleaned_data['toLat'] and self.cleaned_data['toLng']:
            toPoint = Point(self.cleaned_data['toLat'], self.cleaned_data['toLng'])
            sqs = sqs.dwithin('toLocation', fromPoint, 50)
        else:
            toPoint = None

        if self.cleaned_data['leavingOn']:
            sqs = sqs.filter(leavingOn__exact=self.cleaned_data['leavingOn'])
        else:
            sqs = sqs.filter(leavingOn__gte=datetime.date.today())

        return sqs

