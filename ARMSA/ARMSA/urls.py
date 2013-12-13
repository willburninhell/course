from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ARMSA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ABNS/clients/(?P<st>\w{2})/(?P<ho>\d{1,4})/',
        'ABNS.views.ABNS'),
    url(r'^ABNS/search/', 'ABNS.views.search'),
    url(r'^ABNS/', 'ABNS.views.ABNS'),
    url(r'^search/', 'ABNS.views.search'),
    url(r'^clients/(?P<st>\w{2})/(?P<ho>\d{1,4})/', 'ABNS.views.clients'),
    url(r'^clients/', 'ABNS.views.clients'),
    url(r'^delete/', 'ABNS.views.delete_id'),
    url(r'^activate/', 'ABNS.views.activate_id'),
    url(r'^lock/', 'ABNS.views.lock_id'),
    url(r'^portaction/', 'ABNS.views.portaction'),
    url(r'^trustaction/', 'ABNS.views.trustaction'),
    url(r'^ports/(?P<st>\w{2})/(?P<ho>\d{1,4})/', 'ABNS.views.ports'),
    url(r'^ports/', 'ABNS.views.ports'),
    url(r'^switches/(?P<st>\w{2})/(?P<ho>\d{1,4})/', 'ABNS.views.switches'),
    url(r'^switches/', 'ABNS.views.switches'),
    url(r'^macs/(?P<st>\w{2})/(?P<ho>\d{1,4})/', 'ABNS.views.mac'),
    url(r'^macs/', 'ABNS.views.mac'),

)
