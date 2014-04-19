import datetime
from haystack import indexes
from drive.models import Ride


class RideIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    leavingOn = indexes.DateField(model_attr='leavingOn')
    fromLocation = indexes.LocationField()
    toLocation = indexes.LocationField()

    def get_model(self):
        return Ride

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(leavingOn__gte=datetime.date.today())

    def prepare_from_location(self, obj):
        return "%s,%s" % (obj.fromLocation.lat, obj.fromLocation.lng)

    def prepare_to_location(self, obj):
        return "%s,%s" % (obj.toLocation.lat, obj.toLocation.lng)