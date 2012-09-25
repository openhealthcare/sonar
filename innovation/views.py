from django.template.defaultfilters import slugify
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import Item
from forms import ItemForm


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
        form = ItemForm
    context['form'] = form
    return render_to_response('innovation/edit_item.html', context,
        RequestContext(request))

def show_innovation(request, slug):
    """
    Displays a specific innovation.
    """
    item = Item.objects.get(slug=slug)
    return render_to_response('innovation/item.html', {item: item},
        RequestContext(request))
