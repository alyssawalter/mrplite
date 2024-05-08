from django.test import TestCase
from django.urls import reverse
from .models import Item, ItemGroup, UnitOfMeasurement
from .forms import ItemForm, EditItemForm, ItemGroupForm, EditItemGroupForm, \
    UnitOfMeasurementForm, EditUnitOfMeasurementForm
from django.contrib.auth.models import User


class ItemFormTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')
    def test_item_form_valid(self):
        form_data = {
            'item_sku': 'TEST-SKU',
            'item_name': 'Test Item',
            'item_group': ItemGroup.objects.create(item_group_name='Test Group'),
            'unit_of_measurement': UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit'),
            'reorder_point': 10,
            'selling_price': 5.00,
            'manufactured': True,
            'min_qty_for_manufacturing': 20,
            'user': self.user
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        form = ItemForm(data={})
        self.assertFalse(form.is_valid())


class ItemUpdateViewTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password')

        self.item = Item.objects.create(
            item_sku='TEST-SKU',
            item_name='Test Item',
            item_group=ItemGroup.objects.create(item_group_name='Test Group'),
            unit_of_measurement=UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit'),
            reorder_point=10,
            selling_price=5.00,
            manufactured=True,
            min_qty_for_manufacturing=20,
            user=self.user
        )

    def test_item_update_view(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        url = reverse('inventory:edit_item', kwargs={'pk': self.item.item_sku})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_item.html')


class EditItemFormTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create item group
        self.item_group = ItemGroup.objects.create(item_group_name='Test Group')

        # Create unit of measurement
        self.uom = UnitOfMeasurement.objects.create(unit_of_measurement='Test UOM')

        # Create item
        self.item = Item.objects.create(
            item_sku='SKU123',
            item_name='Test Item',
            item_group=self.item_group,
            unit_of_measurement=self.uom,
            reorder_point=10,
            selling_price=100,
            manufactured=True,
            min_qty_for_manufacturing=20,
            user=self.user
        )

        self.valid_data = {
            'item_name': 'Updated Test Item',
            'item_group': self.item_group,
            'reorder_point': 15,
            'selling_price': 150,
            'manufactured': False,
            'min_qty_for_manufacturing': 25,
            'unit_of_measurement': self.uom,
            'user': self.user
        }

        # leaving required info blank
        self.invalid_data = {
            'item_name': '',
            'item_group': '',
            'reorder_point': 'kbojwdv',
            'selling_price': 150,
            'manufactured': "aqdjnw",
            'min_qty_for_manufacturing': 25,
            'unit_of_measurement': self.uom,
        }

    def test_edit_item_form_valid(self):
        # Create form instance with valid data
        form = EditItemForm(instance=self.item, data=self.valid_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_edit_item_form_invalid(self):
        # Create form instance with invalid data
        form = EditItemForm(instance=self.item, data=self.invalid_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())
        # Check if specific fields have errors
        # self.assertIn('item_sku', form.errors)  # Check if item_sku field has error


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


class ItemDeletionTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(item_sku='SKU123', item_name='Test Item',
                                        reorder_point=10, selling_price=100, manufactured=True,
                                        min_qty_for_manufacturing=20)

    def test_item_deletion(self):
        item_count_before = Item.objects.count()
        response = self.client.post(reverse('inventory:item_delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertEqual(Item.objects.count(), item_count_before - 1)  # Item count should decrease by 1


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


class ItemGroupDeletionTests(TestCase):
    def setUp(self):
        self.item_group = ItemGroup.objects.create(item_group_name='Test Group')

        # Create an item assigned to the item group
        self.item = Item.objects.create(item_sku='SKU123', item_name='Test Item', item_group=self.item_group,
                                        reorder_point=10, selling_price=100, manufactured=True,
                                        min_qty_for_manufacturing=20)

    def test_item_group_deletion(self):
        # Get the item's item group before deletion
        item_group_before = self.item.item_group
        # Delete the item group
        response = self.client.post(reverse('inventory:item_group_delete', kwargs={'pk': self.item_group.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        # Refresh the item from the database
        self.item.refresh_from_db()
        # Verify that the item's item group is now null
        self.assertIsNone(self.item.item_group)

        # Verify that the item group count decreased by 1
        item_group_count_before = ItemGroup.objects.count()
        self.assertEqual(item_group_count_before, 0)  # Item group count should be 0 after deletion


class UnitOfMeasurementListViewTests(TestCase):
    def test_unit_of_measurement_list_view(self):
        response = self.client.get(reverse('inventory:unit_of_measurement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['unit_of_measurements'], [])

    def test_unit_of_measurement_detail_view(self):
        unit_of_measurement = UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit')
        response = self.client.get(reverse('inventory:unit_of_measurement_detail', kwargs={'pk': unit_of_measurement.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['unit_of_measurement'], unit_of_measurement)


class CreateUnitOfMeasurementViewTests(TestCase):
    def test_create_unit_of_measurement_view(self):
        response = self.client.get(reverse('inventory:create_unit_of_measurement'))
        self.assertEqual(response.status_code, 200)


class UnitOfMeasurementFormTests(TestCase):
    def test_unit_of_measurement_form_valid(self):
        form_data = {
            'unit_of_measurement': 'Test Unit'
        }
        form = UnitOfMeasurementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_unit_of_measurement_form_invalid(self):
        form = UnitOfMeasurementForm(data={})
        self.assertFalse(form.is_valid())


class EditUnitOfMeasurementViewTests(TestCase):
    def setUp(self):
        self.unit_of_measurement = UnitOfMeasurement.objects.create(unit_of_measurement='Test Unit')

    def test_edit_unit_of_measurement_view(self):
        url = reverse('inventory:edit_unit_of_measurement', kwargs={'pk': self.unit_of_measurement.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/edit_unit_of_measurement.html')

    def test_edit_unit_of_measurement_form_valid(self):
        form_data = {
            'unit_of_measurement': 'Updated Unit'
        }
        url = reverse('inventory:edit_unit_of_measurement', kwargs={'pk': self.unit_of_measurement.pk})
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        updated_unit_of_measurement = UnitOfMeasurement.objects.get(pk=self.unit_of_measurement.pk)
        self.assertEqual(updated_unit_of_measurement.unit_of_measurement, 'Updated Unit')


class EditUnitOfMeasurementFormTests(TestCase):
    def test_edit_unit_of_measurement_form_valid(self):
        form_data = {
            'unit_of_measurement': 'Test Unit'
        }
        form = EditUnitOfMeasurementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_unit_of_measurement_form_invalid(self):
        form = EditUnitOfMeasurementForm(data={})
        self.assertFalse(form.is_valid())


class UnitOfMeasurementDeletionTests(TestCase):
    def test_unit_of_measurement_deletion(self):
        uom = UnitOfMeasurement.objects.create(unit_of_measurement='Test UOM')

        uom_count_before = UnitOfMeasurement.objects.count()
        response = self.client.post(reverse('inventory:unit_of_measurement_delete', kwargs={'pk': uom.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertEqual(UnitOfMeasurement.objects.count(),
                         uom_count_before - 1)  # Unit of measurement count should decrease by 1

    def test_item_uom_null_after_deletion(self):
        uom = UnitOfMeasurement.objects.create(unit_of_measurement='Test UOM 2')
        item = Item.objects.create(item_sku='TestItem', item_name='Test Item', item_group=None, unit_of_measurement=uom,
                                   reorder_point=10, selling_price=100, manufactured=True,
                                   min_qty_for_manufacturing=20)

        uom_count_before = UnitOfMeasurement.objects.count()
        response = self.client.post(reverse('inventory:unit_of_measurement_delete', kwargs={'pk': uom.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertEqual(UnitOfMeasurement.objects.count(),
                         uom_count_before - 1)  # Unit of measurement count should decrease by 1

        # Retrieve the item again from the database to ensure the change is reflected
        item.refresh_from_db()
        self.assertIsNone(item.unit_of_measurement)  # Unit of measurement should be null


class ItemSettingsViewTests(TestCase):
    def test_item_settings_view(self):
        # Access the URL for the item settings page
        response = self.client.get(reverse('inventory:item_settings'))

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'inventory/item_settings.html')