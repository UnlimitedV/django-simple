from django.contrib import admin
from store.models import Collection, Product, Order
from django.db.models import Count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory_status', 'collection_title']
    # sortable_by = ['title']
    list_per_page = 100
    list_select_related = ['collection']
    

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory % 2 == 0:
            return 'even'
        return 'odd'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name']
    list_select_related = ['customer']
    ordering = ['customer']

    def customer_name(self, order):
        fullname = order.customer.first_name + ' ' + order.customer.last_name
        return fullname



@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        return collection.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )