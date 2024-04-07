from django import forms
from .models import Item, ItemGroup


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_sku', 'item_name', 'item_group', 'unit_of_measurement',
                  'reorder_point', 'selling_price', 'manufactured', 'min_qty_for_manufacturing']


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_sku', 'item_name', 'item_group', 'unit_of_measurement',
                  'reorder_point', 'selling_price', 'manufactured', 'min_qty_for_manufacturing']


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['item_group_name']


class EditItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['item_group_name']