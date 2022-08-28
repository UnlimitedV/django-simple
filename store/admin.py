from django.contrib import admin
from store.models import Collection, Product, Order, Customer
from django.db.models import Count, F
from django.db.models.query import QuerySet


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [('%2==0', 'even'), ('%2==1', 'odd')]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '%2==0':
            return queryset.annotate(even=F('inventory')%2).filter(even=False)
        elif self.value() == '%2==1':
            return queryset.annotate(odd=F('inventory')%2).filter(odd=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_per_page = 100
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    sortable_by = ['first_name', 'last_name']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name']