from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Supplier


def suppliers(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add":
            name = request.POST.get("supplier_name", "").strip()
            email = request.POST.get("email", "").strip()
            phone = request.POST.get("phone", "").strip()
            address = request.POST.get("address", "").strip()
            if not all([name, email, phone, address]):
                messages.error(request, "All supplier fields are required.")
            elif Supplier.objects.filter(email__iexact=email).exists():
                messages.error(request, "A supplier with this email already exists.")
            else:
                Supplier.objects.create(supplier_name=name, email=email, phone=phone, address=address)
                messages.success(request, f"{name} was added.")
        elif action == "update":
            supplier = get_object_or_404(Supplier, pk=request.POST.get("supplier_id"))
            supplier.supplier_name = request.POST.get("supplier_name", "").strip()
            supplier.email = request.POST.get("email", "").strip()
            supplier.phone = request.POST.get("phone", "").strip()
            supplier.address = request.POST.get("address", "").strip()
            if not all([supplier.supplier_name, supplier.email, supplier.phone, supplier.address]):
                messages.error(request, "All supplier fields are required.")
            else:
                supplier.save()
                messages.success(request, f"{supplier.supplier_name} was updated.")
        elif action == "delete":
            supplier = get_object_or_404(Supplier, pk=request.POST.get("supplier_id"))
            name = supplier.supplier_name
            try:
                supplier.delete()
                messages.success(request, f"{name} was deleted.")
            except ProtectedError:
                messages.error(request, "Supplier cannot be deleted because products use it.")
        return redirect("suppliers")

    search = request.GET.get("search", "").strip()
    supplier_list = Supplier.objects.all()
    if search:
        supplier_list = supplier_list.filter(supplier_name__icontains=search)
    return render(request, "suppliers/suppliers.html", {"suppliers": supplier_list.order_by("supplier_name"), "search": search, "active": "suppliers"})
