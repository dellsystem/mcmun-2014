from django.conf.urls import patterns, include, url
from mcmun.pages import pages

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cms.views.main'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^loladmin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)
