from django.views.generic import CreateView, TemplateView
from profiles.models import Profile

from .forms import RegisterForm, SocialRegisterForm
from .models import Item


class ProfileCreate(CreateView):
    form_class = SocialRegisterForm
    model = Profile
    template_name = 'profiles/create.html'

    def get_form(self, form_class):
        if hasattr(self.request.user, 'email') and self.request.user.email:
            form_class = RegisterForm
        return super(ProfileCreate, self).get_form(form_class)


class Search(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['term'] = term = self.request.GET.get('term', 'FTW')
        innovats = Item.objects.filter(summary__icontains=term)
        context['innovats'] = innovats
        if len(innovats) > 0:
            innovated = True
        else:
            innovated = False
        context['innovated'] = innovated
        return context


def new_innovation(request):
    """
    Used for adding a new innovation.
    """
    if request.method == 'POST':
        pass
    else:
        pass


def show_innovation(request, ):
    """
    Displays a specific innovation.
    """
    pass

