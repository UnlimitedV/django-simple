from django.contrib import admin
from store.models import Product, Order

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
