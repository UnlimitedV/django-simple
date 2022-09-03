from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset_context(self):
        return {'request': self.request}


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('product')), pk=pk)
        if collection.product_set.count() > 0:
            return Response({"errorr": "Collection can not be deleted becouse it includes one or more products."})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
