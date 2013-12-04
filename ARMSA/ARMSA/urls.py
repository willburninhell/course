from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ARMSA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tree/(?P<st>\w{2})/(?P<ho>\d{1})/', 'ABNS.views.streets_view'),
    url(r'^tree/(?P<st>\w{2})/(?P<ho>\d{2})/', 'ABNS.views.streets_view'),
    url(r'^tree/(?P<st>\w{2})/(?P<ho>\d{3})/', 'ABNS.views.streets_view'),
    url(r'^tree/(?P<st>\w{2})/(?P<ho>\d{4})/', 'ABNS.views.streets_view'),
    url(r'^tree/', 'ABNS.views.streets_view', name='streets_view'),
    url(r'^abns/', 'ABNS.views.abns', name='abns'),
    url(r'^clients/(?P<st>\w{2})/(?P<ho>\d{1})/', 'ABNS.views.clients'),
    url(r'^clients/(?P<st>\w{2})/(?P<ho>\d{2})/', 'ABNS.views.clients'),
    url(r'^clients/(?P<st>\w{2})/(?P<ho>\d{3})/', 'ABNS.views.clients'),
    url(r'^clients/(?P<st>\w{2})/(?P<ho>\d{4})/', 'ABNS.views.clients'),
    url(r'^clients/', 'ABNS.views.clients', name='clients'),
)
