from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from profiles.models import Profile

from forms import RegisterForm, SocialRegisterForm, ItemForm
from models import Item


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


@login_required
def new_innovation(request):
    """
    Used for adding a new innovation.
    """
    context = {}
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = slugify(title)
            created_by = request.user
            summary = form.cleaned_data['summary']
            how_used = form.cleaned_data['how_used']
            benefits = form.cleaned_data['benefits']
            further_information = form.cleaned_data['further_information']
            item = Item.objects.create(title=title, slug=slug,
                created_by=created_by, summary=summary, how_used=how_used,
                benefits=benefits, further_information=further_information)
            tags = form.cleaned_data['tags']
            item.tags.add(*tags)
            return HttpResponseRedirect('/idea/%s' % item.slug)
    else:
        form = ItemForm()
    context['form'] = form
    return render_to_response('innovation/edit_item.html', context,
        RequestContext(request))

def show_innovation(request, slug):
    """
    Displays a specific innovation.
    """
    item = Item.objects.get(slug=slug)
    tags = item.tags.all()
    return render_to_response('innovation/item.html', {'item': item,
        'tags': tags}, RequestContext(request))
