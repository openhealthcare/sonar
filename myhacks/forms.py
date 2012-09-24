from django.forms import ModelForm

from models import Hack


class HackForm(ModelForm):

    class Meta:
        model = Hack
        exclude = ('user',)
