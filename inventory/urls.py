from django.urls import path

from . import views

app_name = "inventory"
urlpatterns = [
    path("", views.items_list, name="items_list"),
    path("item/<str:item_sku>/", views.item_detail, name="item_detail"),
    path("<str:item_sku>/update", views.edit_item, name="edit_item"),
    path("create_item/", views.create_item, name="create_item"),
]