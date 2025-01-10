from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from transactions.models import Transaction
from products.models import Product
from invoices.models import Invoice
from rest_framework_simplejwt.tokens import RefreshToken

class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')

        self.product1 = Product.objects.create(name='Product1', description='Desc1', price=10.00)
        self.product2 = Product.objects.create(name='Product2', description='Desc2', price=20.00)

        self.invoice1 = Invoice.objects.create(user=self.user)
        self.invoice1.products.set([self.product1, self.product2])
        self.invoice1.calculate_total_amount()

        self.invoice2 = Invoice.objects.create(user=self.admin)
        self.invoice2.products.set([self.product1])
        self.invoice2.calculate_total_amount()

        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_access = str(self.user_refresh.access_token)

        self.admin_refresh = RefreshToken.for_user(self.admin)
        self.admin_access = str(self.admin_refresh.access_token)

    def test_create_transaction_for_own_invoice(self):
        url = reverse('transaction-create')
        data = {
            "invoice": self.invoice1.id,
            "amount": "30.00"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Transaction registered successfully.")
        self.assertEqual(response.data['result']['amount'], "30.00")
        self.assertEqual(response.data['result']['invoice_id'], self.invoice1.id)

    def test_create_transaction_for_other_user_invoice(self):
        url = reverse('transaction-create')
        data = {
            "invoice": self.invoice2.id, 
            "amount": "10.00"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Validation error.")
        self.assertIn('invoice', response.data['result'])

    def test_admin_create_transaction_for_any_invoice(self):
        url = reverse('transaction-create')
        data = {
            "invoice": self.invoice2.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Transaction registered successfully.")
        self.assertEqual(Decimal(response.data['result']['amount']), self.invoice2.total_amount)
        self.assertEqual(response.data['result']['invoice_id'], self.invoice2.id)

    def test_view_own_transaction_history(self):
        transaction = Transaction.objects.create(invoice=self.invoice1, amount=30.00)

        url = reverse('transaction-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_access)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Transaction history retrieved successfully.")
        self.assertEqual(len(response.data['result']), 1)
        self.assertEqual(response.data['result'][0]['id'], transaction.id)

    def test_admin_view_all_transaction_history(self):
        Transaction.objects.create(invoice=self.invoice1, amount=30.00)
        Transaction.objects.create(invoice=self.invoice2, amount=15.00)

        url = reverse('transaction-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_access)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Transaction history retrieved successfully.")
        self.assertEqual(len(response.data['result']), 2)
