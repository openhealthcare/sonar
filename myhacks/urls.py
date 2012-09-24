from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import HackView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='myhacks/home.html'), name='home'),
    url('^add$', login_required(HackView.as_view()), name='add'),
    )
