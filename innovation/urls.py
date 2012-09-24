from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),
    # Examples:
    # url(r'^$', 'innovation.views.home', name='home'),
    # url(r'^innovation/', include('innovation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
