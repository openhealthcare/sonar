from django import forms
from profiles.models import Profile

from models import Item


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'affiliation', 'role')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('slug', 'created_by')


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('slug', 'created_by', 'title')

