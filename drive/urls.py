from django.conf.urls import patterns, url
from drive import views
from haystack.views import SearchView
from drive.forms import RideSearchForm

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', views.drive_logout, name='drive_logout'),
    url(r'^rides/new$', views.rides_new, name='rides_new'),
    url(r'^rides/$', views.rides_index, name='rides_index'),
    url(r'^rides/show/(?P<pk>\d+)$', views.rides_show, name='rides_show'),
    url(r'^profile/edit$', views.profile_edit, name='profile_edit'),
    url(r'^rides/search$', SearchView(
        template='search/search.html',
        form_class=RideSearchForm
    ), name='rides_search'),
)
