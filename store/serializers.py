from dataclasses import field
from decimal import Decimal
from store.models import Cart, CartItem, Customer, Product, Collection, Review
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

   
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProduct(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'inventory', 'unit_price']

class ItemSerializer(serializers.ModelSerializer):
    product = SimpleProduct()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, item:CartItem):
        return item.product.unit_price * item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])
        
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']


class AddItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('no product with the given id was found')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_pk']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try: 
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    

class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['user_id', 'id', 'phone', 'birth_date', 'membership']