from django.contrib import admin
from .models import Item, ItemGroup, UnitOfMeasurement

admin.site.register(Item)
admin.site.register(ItemGroup)
admin.site.register(UnitOfMeasurement)