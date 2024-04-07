from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Item, ItemGroup
from .forms import ItemForm, EditItemForm, EditItemGroupForm, ItemGroupForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def items_list(request):
    items = Item.objects.order_by('item_sku')
    return render(request, 'inventory/item_list.html', {'items': items})


def item_detail(request, item_sku):
    try:
        # Retrieve the item object with the given SKU from the database
        item = Item.objects.get(item_sku=item_sku)
    except Item.DoesNotExist:
        raise Http404("Item does not exist")
    # Pass the item object to the template for rendering
    return render(request, 'inventory/item_detail.html', {'item': item})


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save() # Save the form data and get the newly created item instance
            # Redirect to the detail page of the new item
            return HttpResponseRedirect(reverse("inventory:item_detail", args=(new_item.item_sku,)))
    else:
        form = ItemForm()
    return render(request, 'inventory/create_item.html', {'form': form})


def edit_item(request, item_sku):
    item = get_object_or_404(Item, item_sku=item_sku)
    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory:item_detail', item_sku=item_sku)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'inventory/edit_item.html', {'form': form, 'item': item})


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
