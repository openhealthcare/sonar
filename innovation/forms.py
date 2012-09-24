from django import forms
from profiles.models import Profile


class SocialRegisterForm(forms.ModelForm):
    class Meta:
        fields = ('email', 'first_name', 'last_name', 'pseudonym', 'affiliation')
        model = Profile


class RegisterForm(SocialRegisterForm):
    class Meta(SocialRegisterForm.Meta):
        exclude = ('email',)

