from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url('^about$', TemplateView.as_view(template_name='about.html'), name='about'),
    url('^contact$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^accounts/', include('allauth.urls')),
    # Examples:
    # url(r'^$', 'innovation.views.home', name='home'),
    # url(r'^innovation/', include('innovation.foo.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # myhacks
    url(r'^myhacks/', include('myhacks.urls', namespace='myhacks')),

    # innovation management
    url(r'^idea/new/$', 'innovation.views.new_innovation', name='new_idea'),
    url(r'^idea/(?P<slug>[^\.]+)/$', 'innovation.views.show_innovation'),


)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
