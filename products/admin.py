from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "description", "created_at")
    search_fields = ("category_name",)
    ordering = ("category_name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "category", "supplier", "price", "created_at")
    list_filter = ("category", "supplier")
    search_fields = ("product_name", "category__category_name", "supplier__supplier_name")
    ordering = ("product_name",)