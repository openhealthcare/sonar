
from innovation.models import Item

def recent(request):
    return {'ideas': Item.objects.order_by('created_on')[:10]}

