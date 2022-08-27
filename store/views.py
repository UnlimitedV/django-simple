from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection


@api_view(['GET', 'POST'])
def product_list(request: Request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serial = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serial.data)
    elif request.method == 'POST':
        serial = ProductSerializer(data=request.data, context={'request':request})
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.validated_data)
    

@api_view()
def product_detail(request: Request, pk):
    product = get_object_or_404(Product, pk=pk)
    serial = ProductSerializer(product, context={'request':request})
    return Response(serial.data)


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serial = CollectionSerializer(collection)
    return Response(serial.data)

