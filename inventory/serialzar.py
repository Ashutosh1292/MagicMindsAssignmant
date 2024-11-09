# serializers.py

from rest_framework import serializers
from .models import Products , SaleLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price', 'inventory_count', 'category']
class SalelogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleLog
        fields = ['id','product_id','sale_quantity']
