from django.urls import path
from . import views
from .views import *

app_name = "inventory"
urlpatterns = [
    path("", views.items_list, name="items_list"),
    path("item/<str:item_sku>/", views.item_detail, name="item_detail"),
    path("<str:item_sku>/update", views.edit_item, name="edit_item"),
    path("create_item/", views.create_item, name="create_item"),
    path("item_groups/", ItemGroupListView.as_view(), name="item_group_list"),
    path("item_groups/create/", CreateItemGroupView.as_view(), name="create_item_group"),
    path("item_groups/<int:pk>/", ItemGroupDetailView.as_view(), name="item_group_detail"),
    path("item_groups/<int:pk>/edit/", EditItemGroupView.as_view(), name="edit_item_group"),
]