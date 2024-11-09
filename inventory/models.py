from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True) 
    price = models.FloatField()
    inventory_count = models.IntegerField(default=0)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class SaleLog(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    sale_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Sale of {self.product_id}"