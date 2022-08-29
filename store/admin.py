from django.contrib import admin, messages
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

from store.models import Collection, Product, Order, Customer, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [('0', 'even'), ('1', 'odd')]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '0':
            return queryset.annotate(even=F('inventory')%2).filter(even=True)
        elif self.value() == '1':
            return queryset.annotate(even=F('inventory')%2).filter(even=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title']
    list_display = ['id', 'title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_per_page = 100
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['increase_price']
    
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory % 2 == 0:
            return 'even'
        return 'odd'

    def increase_price(self, request, queryset):
        return queryset.update(unit_price=F('unit_price')+1)


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0
    min_num = 1
    max_num = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name']
    list_select_related = ['customer']
    ordering = ['customer']
    inlines = [OrderItemInline]

    def customer_name(self, order):
        fullname = order.customer.first_name + ' ' + order.customer.last_name
        return fullname


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        return collection.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership', 'orders']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )