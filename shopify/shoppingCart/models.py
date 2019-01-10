from django.db import models
from products.models import Product

class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Product)
    total = models.DecimalField(decimal_places=2, max_digits=100)

    def __str__(self):
        return f"Shopping Cart {self.id}, total: {self.total}"
