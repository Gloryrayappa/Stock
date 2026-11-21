from django.shortcuts import render

from inventory.models import Stock


def billing(request):
    billing_rows = [
        {
            "product": stock.product,
            "price": stock.product.price,
            "quantity": stock.quantity,
            "stock_value": stock.product.price * stock.quantity,
            "low_stock": stock.quantity <= stock.reorder_level,
        }
        for stock in Stock.objects.select_related("product").order_by("product__product_name")
    ]
    return render(
        request,
        "billing/billing.html",
        {
            "billing_rows": billing_rows,
            "active": "billing",
        },
    )
