from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import AddView, EditView, HackListView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='myhacks/home.html'),
                                                                name='home'),
    url(r'^add/$', login_required(AddView.as_view()), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', login_required(EditView.as_view()),
                                                                name='edit'),
    url(r'^all$', HackListView.as_view()),
)
