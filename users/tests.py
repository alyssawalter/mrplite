from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthenticationTests(TestCase):
    def test_user_registration(self):
        # Define test user data
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'testpassword'

        # Make a POST request to create a new user
        response = self.client.post(reverse('signup'), {
            'username': username,
            'email': email,
            'password1': password,
            'password2': password,
        })

        # Check if user is created successfully
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(User.objects.filter(username=username).exists())  # User should exist in the database

    def test_user_login(self):
        # Create a test user
        test_user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        # Make a POST request to login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })

        # Check if user is logged in successfully
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # User should be authenticated

    def test_user_logout(self):
        # Create a test user and login
        test_user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Make a POST request to logout
        response = self.client.post(reverse('logout'))

        # Check if user is logged out successfully
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # User should not be authenticated