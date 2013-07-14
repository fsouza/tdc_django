from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tdc.enquetes import views

urlpatterns = patterns('',
                       url(r'^enquetes/(?P<id>\d+)',
                           views.EnqueteView.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
)
