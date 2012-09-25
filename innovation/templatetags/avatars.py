import re
from django import template
import hashlib

register = template.Library()

@register.simple_tag
def avatar(user):
    from allauth.socialaccount.models import SocialAccount
    try:
        acc = SocialAccount.objects.get(user=user)
        return acc.get_avatar_url()
    except SocialAccount.DoesNotExist:
        pass

    h = hashlib.md5((user.email or '').strip().lower()).hexdigest()
    return 'http://www.gravatar.com/avatar/%s' % h


