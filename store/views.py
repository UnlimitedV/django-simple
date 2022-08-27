from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serial = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serial.data)
    
    def post(self, request):
        serial = ProductSerializer(data=request.data, context={'request':request})
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.validated_data)


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serial = ProductSerializer(product, context={'request':request})
        return Response(serial.data)


class CollectionList(APIView):
    def get(self, request):
        collection = Collection.objects.annotate(products_count=Count('product'))
        serial = CollectionSerializer(collection, many=True)
        return Response(serial.data)
    
    def post(self, request):
        serial = CollectionSerializer(data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data)


class CollectionDetail(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        serial = CollectionSerializer(collection)
        return Response(serial.data)

    def patch(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        serial = CollectionSerializer(collection, data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data)
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        if collection.product_set.count() > 0:
            return Response({"errorr": "Collection can not be deleted becouse it includes one or more products."})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
