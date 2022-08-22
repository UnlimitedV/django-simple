from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType

from store.models import Product, OrderItem, Order
from tags.models import TaggedItem


def say_hello(request):
    query = TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, 'hello.html', {'orders': query})
