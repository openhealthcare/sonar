from django.views.generic import CreateView
from profiles.models import Profile

from .forms import RegisterForm, SocialRegisterForm


class ProfileCreate(CreateView):
    form_class = SocialRegisterForm
    model = Profile
    template_name = 'profiles/create.html'

    def get_form(self, form_class):
        if hasattr(self.request.user, 'email') and self.request.user.email:
            form_class = RegisterForm
        return super(ProfileCreate, self).get_form(form_class)

