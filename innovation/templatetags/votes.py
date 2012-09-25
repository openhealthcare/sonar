from django import template

register = template.Library()

@register.simple_tag
def vote_count(target_type, id):
    from innovation.models import Vote
    return Vote.objects.filter(target_type=target_type, target_id=id).count()

@register.simple_tag
def vote_count_for_role(target_type, id, rolename):
    from innovation.models import Vote, Role

    try:
        role = Role.objects.get(name__iexact=rolename)
    except Role.DoesNotExist:
        return 0

    return Vote.objects.filter(target_type=target_type, target_id=id, created_by__role=role).count()

