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
    url(r'^delete/', 'ABNS.views.delete_id'),
    url(r'^clients/', 'ABNS.views.clients'),
    url(r'^ports/(?P<st>\w{2})/(?P<ho>\d{1,4})/', 'ABNS.views.ports'),

)
