from django.db import models
from core.models import DynamicField
class Product(models.Model):
    name = models.CharField(max_length=120)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.barcode}"
    class Meta:
        permissions = [
            ("view_product_public", "Can view products (Public)"),
            ("change_product_user", "Can edit products (User)"),
            ("delete_product_manager", "Can delete products (Manager)"),
        ]

class CustomFieldValueProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dynamic_field = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)  # semua disimpan sebagai teks, tapi bisa dikonversi sesuai tipe
    class Meta:
        db_table = 'custom_field_value_product'
