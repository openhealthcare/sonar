from django import forms
from profiles.models import Profile

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('slug',)


class SocialRegisterForm(forms.ModelForm):
    class Meta:
        fields = ('email', 'first_name', 'last_name', 'pseudonym', 'affiliation')
        model = Profile


class RegisterForm(SocialRegisterForm):
    class Meta(SocialRegisterForm.Meta):
        exclude = ('email',)

