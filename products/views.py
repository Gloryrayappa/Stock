from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from suppliers.models import Supplier
from .models import Category, Product


def categories(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = request.POST.get("category_name", "").strip()
            description = request.POST.get("description", "").strip()
            if not name:
                messages.error(request, "Category name is required.")
            elif Category.objects.filter(category_name__iexact=name).exists():
                messages.error(request, "A category with this name already exists.")
            else:
                Category.objects.create(category_name=name, description=description)
                messages.success(request, f"{name} was added.")
        elif action == "update":
            category = get_object_or_404(Category, pk=request.POST.get("category_id"))
            name = request.POST.get("category_name", "").strip()
            if not name:
                messages.error(request, "Category name is required.")
            else:
                category.category_name = name
                category.description = request.POST.get("description", "").strip()
                category.save(update_fields=["category_name", "description"])
                messages.success(request, f"{name} was updated.")
        elif action == "delete":
            category = get_object_or_404(Category, pk=request.POST.get("category_id"))
            try:
                name = category.category_name
                category.delete()
                messages.success(request, f"{name} was deleted.")
            except ProtectedError:
                messages.error(request, "Category cannot be deleted because products use it.")
        return redirect("categories")

    search = request.GET.get("search", "").strip()
    categories_list = Category.objects.all()
    if search:
        categories_list = categories_list.filter(category_name__icontains=search)
    return render(request, "products/categories.html", {"categories": categories_list.order_by("category_name"), "search": search, "active": "categories"})


def products(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = request.POST.get("product_name", "").strip()
            category_id = request.POST.get("category")
            supplier_id = request.POST.get("supplier")
            price = request.POST.get("price")
            try:
                category = get_object_or_404(Category, pk=category_id)
                supplier = get_object_or_404(Supplier, pk=supplier_id)
                price_value = float(price)
            except (TypeError, ValueError):
                messages.error(request, "Enter a valid product price.")
                return redirect("products")
            if not name:
                messages.error(request, "Product name is required.")
            elif price_value < 0:
                messages.error(request, "Price cannot be negative.")
            else:
                Product.objects.create(
                    product_name=name,
                    category=category,
                    supplier=supplier,
                    description=request.POST.get("description", "").strip(),
                    price=price_value,
                )
                messages.success(request, f"{name} was added.")
        elif action == "update":
            product = get_object_or_404(Product, pk=request.POST.get("product_id"))
            name = request.POST.get("product_name", "").strip()
            try:
                price_value = float(request.POST.get("price"))
            except (TypeError, ValueError):
                messages.error(request, "Enter a valid product price.")
                return redirect("products")
            if not name:
                messages.error(request, "Product name is required.")
            elif price_value < 0:
                messages.error(request, "Price cannot be negative.")
            else:
                product.product_name = name
                product.category = get_object_or_404(Category, pk=request.POST.get("category"))
                product.supplier = get_object_or_404(Supplier, pk=request.POST.get("supplier"))
                product.description = request.POST.get("description", "").strip()
                product.price = price_value
                product.save()
                messages.success(request, f"{name} was updated.")
        elif action == "delete":
            product = get_object_or_404(Product, pk=request.POST.get("product_id"))
            name = product.product_name
            try:
                product.delete()
                messages.success(request, f"{name} was deleted.")
            except ProtectedError:
                messages.error(request, "Product cannot be deleted while it is used by inventory.")
        return redirect("products")

    search = request.GET.get("search", "").strip()
    products_list = Product.objects.select_related("category", "supplier")
    if search:
        from django.db.models import Q

        products_list = products_list.filter(
            Q(product_name__icontains=search)
            | Q(category__category_name__icontains=search)
            | Q(supplier__supplier_name__icontains=search)
        )
    return render(
        request,
        "products/products.html",
        {
            "products": products_list.order_by("product_name"),
            "categories": Category.objects.order_by("category_name"),
            "suppliers": Supplier.objects.order_by("supplier_name"),
            "search": search,
            "active": "products",
        },
    )
