from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ABNS/search/', 'ABNS.views.search'),
    url(r'^ABNS/', 'ABNS.views.ABNS'),
    url(r'^search/', 'ABNS.views.search'),
    url(r'^clients/(?P<st>\w{1,2})/(?P<ho>\d{1,4})/', 'ABNS.views.clients'),
    url(r'^clients/', 'ABNS.views.clients'),
    url(r'^ports/(?P<st>\w{1,2})/(?P<ho>\d{1,4})/', 'ABNS.views.ports'),
    url(r'^ports/', 'ABNS.views.ports'),
    url(r'^switches/(?P<st>\w{1,2})/(?P<ho>\d{1,4})/', 'ABNS.views.switches'),
    url(r'^switches/', 'ABNS.views.switches'),
    url(r'^macs/(?P<st>\w{1,2})/(?P<ho>\d{1,4})/', 'ABNS.views.mac'),
    url(r'^macs/', 'ABNS.views.mac'),
    url(r'^delete_mac/', 'ABNS.views.delete_mac'),
    url(r'^delete/', 'ABNS.views.delete_id'),
    url(r'^activate/', 'ABNS.views.activate_id'),
    url(r'^lock/', 'ABNS.views.lock_id'),
    url(r'^portaction/', 'ABNS.views.portaction'),
    url(r'^trustaction/', 'ABNS.views.trustaction'),
    url(r'^monitor/', 'monitor.views.monitor'),
    url(r'^alarm_info/(?P<id>\d{1,6})', 'monitor.views.alarm_info'),
    url(r'^alarm_update/', 'monitor.views.update'),
    url(r'^show_group/(?P<gr>\d{1,6})', 'monitor.views.show_group'),
)
