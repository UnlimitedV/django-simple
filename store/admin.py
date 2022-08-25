from django.contrib import admin
from store.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'collection']
    sortable_by = ['title']
    list_per_page = 5