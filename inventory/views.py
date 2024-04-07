from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Item, ItemGroup
from .forms import ItemForm, EditItemForm, EditItemGroupForm, ItemGroupForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    ordering = ['item_sku']


class ItemDetailView(DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'
    context_object_name = 'item'


class ItemCreateView(CreateView):
    model = Item
    template_name = 'inventory/create_item.html'
    form_class = ItemForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('inventory:item_detail', kwargs={'pk': self.object.item_sku})


class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'inventory/edit_item.html'
    form_class = EditItemForm
    context_object_name = 'item'

    def get_success_url(self):
        return reverse_lazy('inventory:item_detail', kwargs={'pk': self.object.item_sku})


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
