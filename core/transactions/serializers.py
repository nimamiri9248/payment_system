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
        read_only_fields = ('id', 'status', 'transaction_date')

    def validate_invoice(self, value):
        user = self.context['request'].user
        if not user.is_staff and value.user != user:
            raise serializers.ValidationError("You can only create transactions for your own invoices.")
        return value

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction

class TransactionListSerializer(serializers.ModelSerializer):
    invoice_id = serializers.IntegerField(source='invoice.id', read_only=True)
    invoice_status = serializers.CharField(source='invoice.status', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'invoice_id', 'invoice_status', 'amount', 'status', 'transaction_date')
