# Create your views here.
from django import http
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from forms import HackForm
from models import Hack


class BaseHackView(FormView):
    def get_initial(self):
        initial = {
            'user' : self.request.user,
        }
        past_hack = Hack.objects.filter(user=self.request.user).latest()
        if past_hack:
            initial['where'] = past_hack.where
            initial['what'] = past_hack.what
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return http.HttpResponseRedirect(self.get_success_url())


class AddView(BaseHackView):
    template_name = 'myhacks/add.html'
    form_class = HackForm
    success_url = reverse_lazy('myhacks:home')


class EditView(UpdateView, BaseHackView):
    template_name = 'myhacks/add.html'
    form_class = HackForm
    success_url = reverse_lazy('myhacks:home')
    model = Hack

    def get_object(self):
        return get_object_or_404(self.model,
                                 user=self.request.user,
                                 pk=self.kwargs['pk'])
