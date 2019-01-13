from django.db import models

class Product(models.Model):
    """ Product entity """
    
    id = models.AutoField(primary_key=True)
    title = models.TextField(unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    inventory_count = models.IntegerField()

    def __str__(self):
        return self.title