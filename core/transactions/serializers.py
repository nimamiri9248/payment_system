from rest_framework import serializers
from .models import Transaction
from invoices.models import Invoice

class TransactionCreateSerializer(serializers.ModelSerializer):
    invoice = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ('id', 'invoice', 'amount', 'status', 'transaction_date')
        read_only_fields = ('id', 'status', 'transaction_date', 'amount')

    def validate_invoice(self, value):
        user = self.context['request'].user
        if not user.is_staff and value.user != user:
            raise serializers.ValidationError("You can only create transactions for your own invoices.")
        return value

    def create(self, validated_data):
        invoice = validated_data.get('invoice')
        validated_data['amount'] = invoice.total_amount
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class TransactionListSerializer(serializers.ModelSerializer):
    invoice_id = serializers.IntegerField(source='invoice.id', read_only=True)
    invoice_status = serializers.CharField(source='invoice.status', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'invoice_id', 'invoice_status', 'amount', 'status', 'transaction_date')


class TransactionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('status',)
        
    def validate_status(self, new_status):
        """
        Validate that the status change is allowed:
        - Ensure the new status is a valid choice.
        - Prevent changing status if the current status is COMPLETED or FAILED.
        """
        instance = self.instance
        allowed_statuses = [choice[0] for choice in Transaction.STATUS_CHOICES]
        if new_status not in allowed_statuses:
            raise serializers.ValidationError("Invalid status choice.")

        if instance and instance.status in ['COMPLETED', 'FAILED']:
            raise serializers.ValidationError(
                    "Status cannot be changed once it's COMPLETED or FAILED."
                )
        if new_status == instance.status:
            raise serializers.ValidationError(
                f"Status is already {new_status}."
            )

        return new_status