from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product
from rest_framework_simplejwt.tokens import RefreshToken

class ProductsTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='adminuser', 
            password='adminpass'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser', 
            password='regularpass'
        )
        self.admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_access = str(self.admin_refresh.access_token)

        self.regular_refresh = RefreshToken.for_user(self.regular_user)
        self.regular_access = str(self.regular_refresh.access_token)

        self.list_create_url = reverse('product-list-create') 

    def test_product_list_for_regular_user(self):
        """
        Ensure a regular user can list products (read-only).
        """
        Product.objects.create(name='Prod1', description='Desc1', price=10.0)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.regular_access)
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('result', response.data)
        self.assertTrue(len(response.data['result']) >= 1)

    def test_product_create_for_regular_user_forbidden(self):
        """
        Ensure a regular user cannot create a product (403 Forbidden).
        """
        product_data = {
            "name": "New Product",
            "description": "Desc",
            "price": "19.99"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.regular_access)
        response = self.client.post(self.list_create_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_for_admin_user(self):
        """
        Ensure an admin user can create a product.
        """
        product_data = {
            "name": "Admin Product",
            "description": "Admin Desc",
            "price": "29.99"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access)
        response = self.client.post(self.list_create_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Product created successfully.")
        self.assertEqual(response.data['result']['name'], "Admin Product")

    def test_product_detail_for_admin_user(self):
        """
        Ensure an admin user can retrieve product detail.
        """
        product = Product.objects.create(name='ProdDetail', description='Desc', price=50.0)
        detail_url = reverse('product-detail', args=[product.id])

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access)
        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['result']['name'], "ProdDetail")
