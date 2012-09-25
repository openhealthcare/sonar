from django import template

register = template.Library()

@register.simple_tag
def vote_count(target_type, id):
    from innovation.models import Vote
    return Vote.objects.filter(target_type=target_type, target_id=id).count()

