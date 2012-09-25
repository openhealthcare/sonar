from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import CreateView, TemplateView
from profiles.models import Profile

from forms import RegisterForm, SocialRegisterForm, ItemForm, EditItemForm
from innovation.models import Item, Vote


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

class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self,**kw):
        context = super(Home, self).get_context_data(**kw)
        try:
            showoff = dict(idea=Item.objects.order_by('?').get())
        except Item.DoesNotExist:
            showoff = {'idea' : Item()}
        votes = Vote.objects.filter(target_id=showoff['idea'].id, target_type='item')
        showoff['votes'] = votes
        context['showoff'] = showoff
        context['recent'] = Item.objects.order_by('created_on')[:10]
        context['top'] = list(Item.objects.order_by('created_on'))[-10:]

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
            tags = [t.lower() for t in form.cleaned_data['tags']]
            item.tags.add(*tags)
            messages.info(request, "Success. You have created a new innovation")
            return HttpResponseRedirect('/idea/%s' % item.slug)
    else:
        form = ItemForm()
    context['form'] = form
    context['post_to'] = '/idea/new'
    context['title'] = 'Create new innovation'
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

@login_required
def edit_innovation(request, slug):
    """
    Given an idea identified by a slug will attempt to allow you to edit it.
    """
    item = Item.objects.get(slug=slug)
    if item.created_by != request.user:
        return HttpResponseNotFound()

    context = {}
    if request.method == 'POST':
        form = EditItemForm(request.POST)
        if form.is_valid():
            item.summary = form.cleaned_data['summary']
            item.how_used = form.cleaned_data['how_used']
            item.benefits = form.cleaned_data['benefits']
            item.further_information = form.cleaned_data['further_information']
            item.save()
            tags = [t.lower() for t in form.cleaned_data['tags']]
            item.tags.add(*tags)
            messages.info(request, "Success. You have updated your innovation.")
            return HttpResponseRedirect('/idea/%s' % item.slug)
    else:
        form = EditItemForm(instance=item)
    context['form'] = form
    context['post_to'] = '/idea/edit/%s/' % item.slug
    context['title'] = 'Edit %s' % item.title
    return render_to_response('innovation/edit_item.html', context,
        RequestContext(request))

def show_tagged_with(request, tag):
    """
    Given a tag will display a list of all innovations tagged with it.
    """
    tag = tag.lower()
    items = Item.objects.filter(tags__name__in=[tag])
    return render_to_response('innovation/tagged.html',
        {'items': items, 'tag': tag}, RequestContext(request))
