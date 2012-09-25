from django import forms
from profiles.models import Profile

from models import Item


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'affiliation', 'role')


class CompleteProfileForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        exclude = ('username')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('slug', 'created_by')


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('slug', 'created_by', 'title', 'hero_image')

class HeroImageForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('hero_image',)
        
    hero_image = forms.ImageField(required=False)
    
    def clean_hero_image(self):
        """
        We need to convert the raw image upload (ImageField) in to a path, so
        that when the model is saved, FileBrowser will work. Bit Hacky :/
        """
        data = self.cleaned_data['hero_image']
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        path = default_storage.save('uploads/%s' % data.name,
                                                    ContentFile(data.read()))
        return path
