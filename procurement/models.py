from django.db import models

from django.db import models
from inventory.models import Item  # Import the Item model from the inventory app


class PurchaseTerms(models.Model):
    purchase_term_id = models.AutoField(primary_key=True)
    item_sku = models.ForeignKey(Item, on_delete=models.CASCADE)
    vendor_id = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100)
    vendor_uom = models.CharField(max_length=50)
    conversion_for_uom = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_vendor_uom = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_qty = models.PositiveIntegerField()

    def __str__(self):
        return f"Purchase Term ID: {self.purchase_term_id}"


# Not complete
class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.vendor_name
