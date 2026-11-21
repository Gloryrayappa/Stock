"""
URL configuration for stockwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory.views import dashboard
from products.views import categories, products
from suppliers.views import suppliers
from billing.views import billing
from accounts.views import accounts, signup

admin.site.site_header = "StockWise Administration"
admin.site.site_title = "StockWise Admin"
admin.site.index_title = "Administration Dashboard"

urlpatterns = [
    path('', dashboard, name='inventory-dashboard'),
    path('inventory/', dashboard, name='inventory'),
    path('categories/', categories, name='categories'),
    path('products/', products, name='products'),
    path('suppliers/', suppliers, name='suppliers'),
    path('billing/', billing, name='billing'),
    path('accounts/', accounts, name='accounts'),
    path('signup/', signup, name='signup'),
    path('admin/', admin.site.urls),
]
