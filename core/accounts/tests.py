from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class AccountsTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.profile_url = reverse('profile')

        self.user_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.save()

    def test_user_registration(self):
        """
        Ensure a new user can register successfully.
        """
        data = {
            "username": "newuser",
            "password": "newpass123",
            "confirm_password": "newpass123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "User registered successfully.")

    def test_user_login(self):
        """
        Ensure a registered user can obtain JWT tokens.
        """
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_profile_retrieve(self):
        """
        Ensure a user can retrieve their profile information.
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('result', response.data)
        self.assertEqual(response.data['result']['username'], "testuser")

    def test_user_profile_update(self):
        """
        Ensure a user can update their profile information (PATCH).
        """
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        patch_data = {"email": "updated@example.com"}
        response = self.client.patch(self.profile_url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('result', response.data)
        self.assertEqual(response.data['result']['email'], "updated@example.com")
