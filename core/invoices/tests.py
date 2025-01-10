from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from invoices.models import Invoice
from products.models import Product

class InvoicesTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='invoiceuser', password='invoicepass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')

        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)

        self.admin_refresh = RefreshToken.for_user(self.admin_user)
        self.admin_access = str(self.admin_refresh.access_token)

        self.invoice_list_create_url = reverse('invoice-list-create')

        self.product1 = Product.objects.create(name="Prod1", description="Desc1", price=10.0)
        self.product2 = Product.objects.create(name="Prod2", description="Desc2", price=20.0)

    def test_invoice_create_user(self):
        """
        Ensure a regular user can create an invoice for themselves.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access)
        data = {
            "products": [self.product1.id, self.product2.id],
            "status": "PENDING"
        }
        response = self.client.post(self.invoice_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('result', response.data)
        self.assertTrue(len(response.data['result']['products_info']) == 2)

    def test_invoice_list_user(self):
        """
        Ensure a user sees only their own invoices.
        """
        invoice_user = Invoice.objects.create(user=self.user)
        invoice_user.products.set([self.product1])
        invoice_user.calculate_total_amount()

        invoice_admin = Invoice.objects.create(user=self.admin_user)
        invoice_admin.products.set([self.product2])
        invoice_admin.calculate_total_amount()

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access)
        response = self.client.get(self.invoice_list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['result']), 1)

    def test_invoice_list_admin(self):
        """
        Ensure an admin sees all invoices.
        """
        Invoice.objects.create(user=self.user)
        Invoice.objects.create(user=self.admin_user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access)
        response = self.client.get(self.invoice_list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['result']) >= 2) 
