from django.db import models

class Product(models.Model):
    title = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory_count = models.IntegerField()