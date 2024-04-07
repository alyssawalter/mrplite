from django.test import TestCase
from django.urls import reverse
from .models import Item, ItemGroup, UnitOfMeasurement
from .forms import ItemForm, EditItemForm, ItemGroupForm, EditItemGroupForm


class ItemFormTests(TestCase):
    def test_item_form_valid(self):
        form_data = {
            'item_sku': 'TEST-SKU',
            'item_name': 'Test Item',
            'item_group': ItemGroup.objects.create(item_group_name='Test Group'),
            'unit_of_measurement': UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit'),
            'reorder_point': 10,
            'selling_price': 5.00,
            'manufactured': True,
            'min_qty_for_manufacturing': 20
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        form = ItemForm(data={})
        self.assertFalse(form.is_valid())


class ItemUpdateViewTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            item_sku='TEST-SKU',
            item_name='Test Item',
            item_group=ItemGroup.objects.create(item_group_name='Test Group'),
            unit_of_measurement=UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit'),
            reorder_point=10,
            selling_price=5.00,
            manufactured=True,
            min_qty_for_manufacturing=20
        )

    def test_item_update_view(self):
        url = reverse('inventory:edit_item', kwargs={'pk': self.item.item_sku})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item.html')

    def test_item_update_form_valid(self):
        form_data = {
            'item_name': 'Updated Item',
            'reorder_point': 15
            # Add other fields as needed
        }
        url = reverse('inventory:edit_item', kwargs={'pk': self.item.item_sku})
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        updated_item = Item.objects.get(item_sku='UPDATED-SKU')
        self.assertEqual(updated_item.item_name, 'Updated Item')
        self.assertEqual(updated_item.reorder_point, 15)


class EditItemFormTests(TestCase):

    def setUp(self):
        self.item = Item.objects.create(item_sku='SKU123', item_name='Test Item', item_group=ItemGroup.objects.create(item_group_name='Test Group'), reorder_point=10, selling_price=100, manufactured=True, min_qty_for_manufacturing=20)
        self.valid_data = {
            'item_name': 'Updated Test Item',
            'item_group': self.item.item_group.id,  # Use existing item_group id
            'reorder_point': 15,
            'selling_price': 150,
            'manufactured': False,
            'min_qty_for_manufacturing': 25
        }
        self.invalid_data = {
            'item_sku': 'NewSKU',  # Attempting to update SKU (PK)
            'item_name': 'Updated Test Item',
            'item_group': self.item.item_group.id,
            'reorder_point': 15,
            'selling_price': 150,
            'manufactured': False,
            'min_qty_for_manufacturing': 25
        }
    def test_edit_item_form_valid(self):
        # Create some initial data
        initial_data = {
            'item_name': 'Test Item',
            'reorder_point': 10
            # Add other fields as needed
        }
        # Create an instance of the form with initial data
        form = EditItemForm(data=initial_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_edit_item_form_invalid(self):
        # Create some initial data with invalid values
        invalid_data = {
            'item_sku': '',  # Invalid SKU (empty)
            'item_name': 'Test Item',
            'reorder_point': -5  # Invalid reorder point (negative)
            # Add other fields as needed
        }
        # Create an instance of the form with invalid data
        form = EditItemForm(data=invalid_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())
        # Check if specific fields have errors
        self.assertIn('item_sku', form.errors)  # Check if item_sku field has error
        self.assertIn('reorder_point', form.errors)  # Check if reorder_point field has error


class ItemListViewTests(TestCase):
    def setUp(self):
        self.item_group = ItemGroup.objects.create(item_group_name='Test Group')
        self.unit_of_measurement = UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit')

    def test_item_list_view(self):
        response = self.client.get(reverse('inventory:item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['items'], [])

    def test_item_detail_view(self):
        item = Item.objects.create(item_sku='TEST-SKU', item_name='Test Item', item_group=self.item_group,
                                   unit_of_measurement=self.unit_of_measurement, reorder_point=10, selling_price=5.00,
                                   manufactured=True, min_qty_for_manufacturing=20)
        response = self.client.get(reverse('inventory:item_detail', kwargs={'pk': item.item_sku}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item'], item)


class CreateItemViewTests(TestCase):
    def test_item_create_view(self):
        response = self.client.get(reverse('inventory:create_item'))
        self.assertEqual(response.status_code, 200)


class ItemGroupListViewTests(TestCase):
    def test_item_group_list_view(self):
        response = self.client.get(reverse('inventory:item_group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['item_groups'], [])

    def test_item_group_detail_view(self):
        item_group = ItemGroup.objects.create(item_group_name='Test Group')
        response = self.client.get(reverse('inventory:item_group_detail', kwargs={'pk': item_group.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['item_group'], item_group)


class CreateItemGroupViewTests(TestCase):
    def test_create_item_group_view(self):
        response = self.client.get(reverse('inventory:create_item_group'))
        self.assertEqual(response.status_code, 200)


class ItemGroupFormTests(TestCase):
    def test_item_group_form_valid(self):
        form_data = {
            'item_group_name': 'Test Group'
        }
        form = ItemGroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_group_form_invalid(self):
        form = ItemGroupForm(data={})
        self.assertFalse(form.is_valid())


class EditItemGroupViewTests(TestCase):
    def setUp(self):
        self.item_group = ItemGroup.objects.create(item_group_name='Test Group')

    def test_item_group_update_view(self):
        url = reverse('inventory:edit_item_group', kwargs={'pk': self.item_group.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item_group.html')

    def test_item_group_update_form_valid(self):
        form_data = {
            'item_group_name': 'Updated Group Name'
        }
        url = reverse('inventory:edit_item_group', kwargs={'pk': self.item_group.pk})
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        updated_item_group = ItemGroup.objects.get(pk=self.item_group.pk)
        self.assertEqual(updated_item_group.item_group_name, 'Updated Group Name')


class EditItemGroupFormTests(TestCase):
    def test_edit_item_group_form_valid(self):
        # Create some initial data
        initial_data = {
            'item_group_name': 'Test Group'
            # Add other fields as needed
        }
        # Create an instance of the form with initial data
        form = EditItemGroupForm(data=initial_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_edit_item_group_form_invalid(self):
        # Create some initial data with invalid values
        invalid_data = {
            'item_group_name': ''  # Invalid group name (empty)
            # Add other fields as needed
        }
        # Create an instance of the form with invalid data
        form = EditItemGroupForm(data=invalid_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())
        # Check if specific fields have errors
        self.assertIn('item_group_name', form.errors)  # Check if item_group_name field has error
