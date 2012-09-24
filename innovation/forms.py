from django.forms import ModelForm
from innovation.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
