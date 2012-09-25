from django import template

register = template.Library()

@register.simple_tag
def screen_name(user):
    from allauth.socialaccount.models import SocialAccount

    name = user.username

    try:
        acc = SocialAccount.objects.get(user=user.id)
        url =  acc.get_profile_url()
        twitter = 'http://twitter.com/'
        if url.startswith(twitter):
            name = "@%s" % url[len(twitter):]
    except SocialAccount.DoesNotExist:
        pass

    return name
