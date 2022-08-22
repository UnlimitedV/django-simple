from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

from store.models import Product, OrderItem, Order
from tags.models import TaggedItem


def say_hello(request):
    content_type = ContentType.objects.get_for_model(Product)
    query = TaggedItem.objects.select_related('tag').filter(
        content_type = content_type, 
        object_id = 8
    )
    return render(request, 'hello.html', {'orders': query})
