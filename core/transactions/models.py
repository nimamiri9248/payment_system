from decimal import Decimal
from django.db import models
from invoices.models import Invoice
from django.core.validators import MinValueValidator

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.pk} - Invoice #{self.invoice.pk} - {self.status}"
