from django.contrib import admin
from store.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory_status']
    # sortable_by = ['title']
    list_per_page = 15
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory % 2 == 0:
            return 'even'
        return 'odd'