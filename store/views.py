from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import ProductSerializer
from .models import Product


@api_view()
def product_list(request: Request):
    queryset = Product.objects.select_related('collection').all()
    serial = ProductSerializer(queryset, many=True)
    return Response(serial.data)


@api_view()
def product_detail(request: Request, pk):
    product = get_object_or_404(Product, pk=pk)
    serial = ProductSerializer(product)
    return Response(serial.data)