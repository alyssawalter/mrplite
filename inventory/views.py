from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Item, ItemGroup, UnitOfMeasurement
from .forms import ItemForm, EditItemForm, \
    EditItemGroupForm, ItemGroupForm, \
    UnitOfMeasurementForm, EditUnitOfMeasurementForm, \
    InventoryQuantityForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    ordering = ['item_sku']


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'
    context_object_name = 'item'


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'inventory/create_item.html'
    form_class = ItemForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('inventory:item_detail', kwargs={'pk': self.object.item_sku})


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    template_name = 'inventory/edit_item.html'
    form_class = EditItemForm
    context_object_name = 'item'

    def get_success_url(self):
        return reverse_lazy('inventory:item_detail', kwargs={'pk': self.object.item_sku})


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('inventory:item_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ItemGroupListView(ListView):
    model = ItemGroup
    template_name = 'inventory/item_group_list.html'
    context_object_name = 'item_groups'


class ItemGroupDetailView(DetailView):
    model = ItemGroup
    template_name = 'inventory/item_group_detail.html'
    context_object_name = 'item_group'


class CreateItemGroupView(CreateView):
    model = ItemGroup
    form_class = ItemGroupForm
    template_name = 'inventory/create_item_group.html'

    def get_success_url(self):
        return reverse_lazy('inventory:item_group_detail', kwargs={'pk': self.object.pk})


class EditItemGroupView(UpdateView):
    model = ItemGroup
    form_class = EditItemGroupForm
    template_name = 'inventory/edit_item_group.html'
    context_object_name = 'item_group'

    def get_success_url(self):
        return reverse_lazy('inventory:item_group_detail', kwargs={'pk': self.object.pk})


class ItemGroupDeleteView(DeleteView):
    model = ItemGroup
    template_name = 'inventory/item_group_confirm_delete.html'
    success_url = reverse_lazy('inventory:item_group_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Item group deleted successfully.')
        return super().delete(request, *args, **kwargs)


class UnitOfMeasurementListView(ListView):
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_list.html'
    context_object_name = 'unit_of_measurements'


class UnitOfMeasurementDetailView(DetailView):
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_detail.html'
    context_object_name = 'unit_of_measurement'


class CreateUnitOfMeasurementView(CreateView):
    model = UnitOfMeasurement
    form_class = UnitOfMeasurementForm
    template_name = 'inventory/create_unit_of_measurement.html'

    def get_success_url(self):
        return reverse_lazy('inventory:unit_of_measurement_detail', kwargs={'pk': self.object.pk})


class EditUnitOfMeasurementView(UpdateView):
    model = UnitOfMeasurement
    form_class = EditUnitOfMeasurementForm
    template_name = 'inventory/edit_unit_of_measurement.html'
    context_object_name = 'unit_of_measurement'

    def get_success_url(self):
        return reverse_lazy('inventory:unit_of_measurement_detail', kwargs={'pk': self.object.pk})


class UnitOfMeasurementDeleteView(DeleteView):
    model = UnitOfMeasurement
    template_name = 'inventory/unit_of_measurement_confirm_delete.html'
    success_url = reverse_lazy('inventory:unit_of_measurement_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Unit of measurement deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ItemSettingsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'item_group_list_url': reverse_lazy('inventory:item_group_list'),
            'unit_of_measurement_list_url': reverse_lazy('inventory:unit_of_measurement_list'),
        }
        return render(request, 'inventory/item_settings.html', context)


def inventory(request):
    items = Item.objects.order_by('item_sku')
    if request.method == 'POST':
        form = InventoryQuantityForm(request.POST)
        print(request.POST)
        if form.is_valid():
            item_sku = request.POST.get('item_sku')
            print(item_sku)
            new_quantity = form.cleaned_data['quantity']
            item = Item.objects.get(item_sku=item_sku)
            item.quantity = new_quantity
            item.save()
            return redirect('inventory:inventory')  # Redirect to the inventory page after updating quantity
    else:
        form = InventoryQuantityForm()
    return render(request, 'inventory/inventory.html', {'items': items, 'inventory_form': form})

