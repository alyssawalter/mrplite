from django.db import models
from django.contrib.auth.models import User


class ItemGroup(models.Model):
    item_group_number = models.AutoField(primary_key=True)
    item_group_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.item_group_name


class UnitOfMeasurement(models.Model):
    unit_of_measurement_id = models.AutoField(primary_key=True)
    unit_of_measurement = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.unit_of_measurement


class Item(models.Model):
    item_sku = models.CharField(max_length=50, primary_key=True)
    item_name = models.CharField(max_length=100, blank=True, null=True)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, blank=True, null=True)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.SET_NULL, blank=True, null=True)
    reorder_point = models.PositiveIntegerField(blank=True, null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    manufactured = models.BooleanField(blank=True, null=True)
    min_qty_for_manufacturing = models.PositiveIntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.item_name

