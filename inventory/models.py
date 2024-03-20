from django.db import models


class ItemGroup(models.Model):
    item_group_number = models.AutoField(primary_key=True)
    item_group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_group_name


class UnitOfMeasurement(models.Model):
    unit_of_measurement_id = models.AutoField(primary_key=True)
    unit_of_measurement = models.CharField(max_length=50)

    def __str__(self):
        return self.unit_of_measurement


class Item(models.Model):
    item_sku = models.CharField(max_length=50, primary_key=True)
    item_name = models.CharField(max_length=100)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    unit_of_measurement = models.ForeignKey(UnitOfMeasurement, on_delete=models.CASCADE)
    reorder_point = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufactured = models.BooleanField()
    min_qty_for_manufacturing = models.PositiveIntegerField()

    def __str__(self):
        return self.item_name
