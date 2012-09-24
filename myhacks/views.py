# Create your views here.
from django.views.generic.edit import FormView
from forms import HackForm

class HackView(FormView):
    template_name = 'myhacks/add.html'
    form_class = HackForm
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return http.HttpResponseRedirect(self.get_success_url())
    