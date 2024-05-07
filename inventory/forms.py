from django import forms
from .models import Item, ItemGroup, UnitOfMeasurement


class ItemForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['item_group'].queryset = ItemGroup.objects.filter(user=user)
        self.fields['unit_of_measurement'].queryset = UnitOfMeasurement.objects.filter(user=user)
    class Meta:
        model = Item
        fields = ['item_sku', 'item_name', 'item_group', 'unit_of_measurement',
                  'reorder_point', 'selling_price', 'manufactured', 'min_qty_for_manufacturing']


class EditItemForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.fields['item_group'].queryset = ItemGroup.objects.filter(user=user)
        self.fields['unit_of_measurement'].queryset = UnitOfMeasurement.objects.filter(user=user)

    # cant update the sku
    class Meta:
        model = Item
        fields = ['item_name', 'item_group', 'unit_of_measurement',
                  'reorder_point', 'selling_price', 'manufactured', 'min_qty_for_manufacturing']


class InventoryQuantityForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['quantity']


class ItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['item_group_name']


class EditItemGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['item_group_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_group_name'].required = True  # Make item_group_name field required


class UnitOfMeasurementForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasurement
        fields = ['unit_of_measurement']


class EditUnitOfMeasurementForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasurement
        fields = ['unit_of_measurement']