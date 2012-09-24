from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='myhacks/home.html'), name='home'),
    url('^add$', TemplateView.as_view(template_name='myhacks/add.html'), name='home'),
    )
