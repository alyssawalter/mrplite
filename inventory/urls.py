from django.urls import path
from . import views
from .views import *

app_name = "inventory"
urlpatterns = [
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/create/', ItemCreateView.as_view(), name='create_item'),
    path('items/<str:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/<str:pk>/edit/', ItemUpdateView.as_view(), name='edit_item'),
    path("item_groups/", ItemGroupListView.as_view(), name="item_group_list"),
    path("item_groups/create/", CreateItemGroupView.as_view(), name="create_item_group"),
    path("item_groups/<int:pk>/", ItemGroupDetailView.as_view(), name="item_group_detail"),
    path("item_groups/<int:pk>/edit/", EditItemGroupView.as_view(), name="edit_item_group"),
]
