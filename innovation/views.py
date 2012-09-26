from allauth.account import signals
from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation, user_display
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, TemplateView, UpdateView
from profiles.models import Profile

from .forms import CompleteProfileForm, ItemForm, EditItemForm, HeroImageForm, ProfileForm
from .models import Item, Vote
from .utils import method_decorator


class AuthMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthMixin, self).dispatch(request, *args, **kwargs)


class ProfileIncompleteMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'profile') and not isinstance(request.user, AnonymousUser):
            return CompleteProfile.dispatch(CompleteProfile(), request, *args, **kwargs)
        return super(ProfileIncompleteMixin, self).dispatch(request, *args, **kwargs)


class CompleteProfile(CreateView):
    form_class = CompleteProfileForm
    model = Profile
    success_url = '/'
    template_name = 'account/complete_profile.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_ptr = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        initial = super(CompleteProfile, self).get_initial()
        initial['email'] = self.request.user.email
        return initial


class SignUp(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('complete_profile')
    template_name = 'account/signup.html'

    def get_form_kwargs(self):
        kwargs = super(SignUp, self).get_form_kwargs()
        try:
            del kwargs['instance']  # bad allauth
        except KeyError:
            pass
        return kwargs

    def form_valid(self, form):
        """Create and log in the user signing up

        Took this from allauth because extensibility is for chumps.
        """
        self.object = form.save(request=self.request)
        signals.user_signed_up.send(sender=self.object.__class__,
                                    request=self.request,
                                    user=self.object)

        # not is_active: social users are redirected to a template
        # local users are stopped due to form validation checking is_active
        assert self.object.is_active
        if (settings.ACCOUNT_EMAIL_VERIFICATION
            and not EmailAddress.objects.filter(user=self.object,
                                                verified=True).exists()):
            send_email_confirmation(self.object, self.request)

        # HACK: This may not be nice. The proper Django way is to use an
        # authentication backend, but I fail to see any added benefit
        # whereas I do see the downsides (having to bother the integrator
        # to set up authentication backends in settings.py
        if not hasattr(self.object, 'backend'):
            self.object.backend = "django.contrib.auth.backends.ModelBackend"
        signals.user_logged_in.send(sender=self.object.__class__,
                                    request=self.request,
                                    user=self.object)
        login(self.request, self.object)
        msg = _('Successfully signed in as {0}.'.format(user_display(self.object)))
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.get_success_url())


class Search(ProfileIncompleteMixin, TemplateView):
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
        except Item.MultipleObjectsReturned:
            showoff = dict(idea=Item.objects.order_by('?')[0])
        votes = Vote.objects.filter(target_id=showoff['idea'].id, target_type='item')
        showoff['votes'] = votes
        context['showoff'] = showoff
        context['recent'] = Item.objects.order_by('created_on')[:10]
        context['top'] = list(Item.objects.order_by('created_on'))[-10:]

        return context

# TODO: CBV & add ProfileIncompleteMixin
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
    context['post_to'] = '/idea/new/'
    context['title'] = 'Create new innovation'
    return render_to_response('innovation/edit_item.html', context,
        RequestContext(request))

class ShowInnovation(ProfileIncompleteMixin, UpdateView):
    model = Item
    template_name = 'innovation/item.html'
    form_class = HeroImageForm

    def get_context_data(self, **kwargs):
        context = super(ShowInnovation, self).get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()
        return context

# TODO: CBV & add ProfileIncompleteMixin
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

# TODO: CBV & add ProfileIncompleteMixin
def show_tagged_with(request, tag):
    """
    Given a tag will display a list of all innovations tagged with it.
    """
    tag = tag.lower()
    items = Item.objects.filter(tags__name__in=[tag])
    return render_to_response('innovation/tagged.html',
        {'items': items, 'tag': tag}, RequestContext(request))

# TODO: CBV & add ProfileIncompleteMixin
@login_required
def vote_up(request, target_type, target_id):
    import json
    from .models import Vote

    if Vote.objects.filter(target_type=target_type).\
            filter(created_by=request.user).\
            filter(target_id=target_id).count() == 0:
        Vote.objects.create(target_type=target_type,
                            target_id=target_id,
                            created_by=request.user)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))


class EditProfile(AuthMixin, ProfileIncompleteMixin, UpdateView):
    form_class = ProfileForm
    model = Profile
    success_url = reverse_lazy('edit_profile')
    template_name = 'account/edit.html'

    def get_object(self):
        return self.request.user.profile


def show_user_profile(request, username):
    """
    Given a username, displays a page full of information about them.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    return render_to_response('innovation/user_profile.html',
        {'user': user}, RequestContext(request))
