import datetime
from haystack import indexes
from drive.models import Ride


class RideIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    leavingOn = indexes.DateField(model_attr='leavingOn')
    fromLocation = indexes.LocationField(model_attr='fromLocation__get_location')
    toLocation = indexes.LocationField(model_attr='toLocation__get_location')

    def get_model(self):
        return Ride

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(leavingOn__gte=datetime.date.today())
