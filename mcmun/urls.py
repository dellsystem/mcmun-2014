from django.conf.urls import patterns, include, url
from django.contrib import admin

from mcmun.conf import ADMIN_PREFIX
from mcmun.pages import pages

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'cms.views.main', name='home'),
    url(r'^dashboard', 'mcmun.views.dashboard', name='dashboard'),
    url(r'^merchandise-submit', 'merchandise.views.submit', name='merchandise_submit'),
    url(r'^merchandise-order', 'merchandise.views.order', name='merchandise_order'),
    url(r'^merchandise', 'merchandise.views.main', name='merchandise'),
    url(r'^event-registration', 'mcmun.views.events', name='events'),
    url(r'^committee-prefs', 'mcmun.views.committee_prefs', name='committee_prefs'),
    url(r'^assignments', 'mcmun.views.assignments', name='assignments'),
    url(r'^%s/' % ADMIN_PREFIX, include(admin.site.urls)),
    url(r'^committees/', include('committees.urls')),
    url(r'^staff-application/', include('staffapps.urls')),
    url(r'^signups/', include('signups.urls')),
    url(r'^twitter/', include('twitter.urls')),
    #url(r'^registration', 'mcmun.views.registration', name='registration'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password$', 'django.contrib.auth.views.password_change', {'template_name': 'password.html'}, name='password'),
    url(r'^password_success$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_success.html'}, name="password_success"),
    url(r'^position-papers/(?P<file_name>[^/]+)', 'committees.views.serve_papers'),
    url(r'^search', 'search.views.search', name='search'),
    url(r'^', include('cms.urls')),
)
