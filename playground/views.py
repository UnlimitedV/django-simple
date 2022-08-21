from django.shortcuts import render
from django.http import HttpResponse

from store.models import Product, OrderItem, Order


def say_hello(request):
    query = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('-placed_at')[:5]
    return render(request, 'hello.html', {'orders': query})
