from django.db import models
from products.models import Product


class Stock(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=5)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name