from django.contrib import messages
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import Stock


def dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            product_id = request.POST.get("product")
            quantity = request.POST.get("quantity", "0")
            reorder_level = request.POST.get("reorder_level", "5")

            try:
                quantity = int(quantity)
                reorder_level = int(reorder_level)
                product = get_object_or_404(Product, pk=product_id)
            except (TypeError, ValueError):
                messages.error(request, "Quantity and reorder level must be valid numbers.")
                return redirect("inventory-dashboard")

            if quantity < 0 or reorder_level < 0:
                messages.error(request, "Quantity and reorder level cannot be negative.")
            elif hasattr(product, "stock"):
                messages.error(request, "This product already has a stock record.")
            else:
                Stock.objects.create(
                    product=product,
                    quantity=quantity,
                    reorder_level=reorder_level,
                )
                messages.success(request, f"Stock created for {product.product_name}.")

        elif action == "update":
            stock = get_object_or_404(Stock, pk=request.POST.get("stock_id"))
            try:
                quantity = int(request.POST.get("quantity", "0"))
                reorder_level = int(request.POST.get("reorder_level", "5"))
            except (TypeError, ValueError):
                messages.error(request, "Quantity and reorder level must be valid numbers.")
                return redirect("inventory-dashboard")

            if quantity < 0 or reorder_level < 0:
                messages.error(request, "Quantity and reorder level cannot be negative.")
            else:
                stock.quantity = quantity
                stock.reorder_level = reorder_level
                stock.save(update_fields=["quantity", "reorder_level", "updated_at"])
                messages.success(request, f"{stock.product.product_name} was updated.")

        elif action == "delete":
            stock = get_object_or_404(Stock, pk=request.POST.get("stock_id"))
            product_name = stock.product.product_name
            stock.delete()
            messages.success(request, f"Stock record for {product_name} was deleted.")

        return redirect("inventory-dashboard")

    search = request.GET.get("search", "").strip()
    stocks = Stock.objects.select_related("product", "product__category", "product__supplier")
    if search:
        stocks = stocks.filter(
            Q(product__product_name__icontains=search)
            | Q(product__category__category_name__icontains=search)
            | Q(product__supplier__supplier_name__icontains=search)
        )

    available_products = Product.objects.exclude(stock__isnull=False).select_related(
        "category", "supplier"
    ).order_by("product_name")

    return render(
        request,
        "inventory/dashboard.html",
        {
            "stocks": stocks.order_by("product__product_name"),
            "available_products": available_products,
            "search": search,
            "low_stock_count": Stock.objects.filter(quantity__lte=F("reorder_level")).count(),
            "active": "inventory",
        },
    )
