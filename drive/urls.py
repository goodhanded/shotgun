from django.conf.urls import patterns, url
from drive import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', views.drive_logout, name='drive_logout'),
    url(r'^rides/new$', views.rides_new, name='rides_new'),
)
