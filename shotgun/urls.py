from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shotgun.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^', include('drive.urls')),
    (r'^search/', include('haystack.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^login/$',  login),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT,}),
)
