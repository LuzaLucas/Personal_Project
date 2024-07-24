from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'stock', 'is_published', 
        'category', 'updated_at')
    prepopulated_fields = {'slug': ('name',)} 
    list_editable = ('is_published', 'category')
    readonly_fields = ('created_at', 'updated_at')
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    