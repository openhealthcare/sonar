from allauth.account import signals
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation, user_display
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import CompleteProfileForm
from .models import Item, Profile


class CompleteProfile(UpdateView):
    form_class = CompleteProfileForm
    model = Profile
    template_name = 'account/complete_profile.html'

    def get_object(self, *args, **kwargs):
        return self.request.user


class SignUp(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('complete_profile')
    template_name = 'account/signup.html'

    def get_form_kwargs(self):
        kwargs = super(SignUp, self).get_form_kwargs()
        try:
            del kwargs['instance']  # bad allauth
        except KeyError:
            pass
        return kwargs

    def form_valid(self, form):
        """Create and log in the user signing up

        Took this from allauth because extensibility is for chumps.
        """
        self.object = form.save(request=self.request)
        signals.user_signed_up.send(sender=self.object.__class__,
                                    request=self.request,
                                    user=self.object)

        # not is_active: social users are redirected to a template
        # local users are stopped due to form validation checking is_active
        assert self.object.is_active
        if (settings.ACCOUNT_EMAIL_VERIFICATION
            and not EmailAddress.objects.filter(user=self.object,
                                                verified=True).exists()):
            send_email_confirmation(self.object, self.request)

        # HACK: This may not be nice. The proper Django way is to use an
        # authentication backend, but I fail to see any added benefit
        # whereas I do see the downsides (having to bother the integrator
        # to set up authentication backends in settings.py
        if not hasattr(self.object, 'backend'):
            self.object.backend = "django.contrib.auth.backends.ModelBackend"
        signals.user_logged_in.send(sender=self.object.__class__,
                                    request=self.request,
                                    user=self.object)
        login(self.request, self.object)
        msg = _('Successfully signed in as {0}.'.format(user_display(self.object)))
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.get_success_url())


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

