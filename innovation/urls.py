from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^$', 'innovation.views.home', name='home'),
    # url(r'^innovation/', include('innovation.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
