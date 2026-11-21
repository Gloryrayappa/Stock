from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "reorder_level", "stock_status", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("product__product_name", "product__category__category_name")
    list_editable = ("quantity", "reorder_level")
    ordering = ("product__product_name",)

    @admin.display(boolean=True, description="In stock")
    def stock_status(self, obj):
        return obj.quantity > obj.reorder_level