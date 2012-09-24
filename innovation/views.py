from django.template.defaultfilters import slugify
from django.views.generic import TemplateView
from models import Item
from forms import ItemForm

class Search(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['term'] = term = self.request.GET.get('term', 'FTW')
        innovats = Item.objects.filter(summary__contains=term)
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
