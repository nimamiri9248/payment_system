from rest_framework import serializers
from products.models import Product
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Invoice
        fields = (
            'id',
            'user',
            'products',
            'total_amount',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'total_amount', 'created_at', 'updated_at')

    def create(self, validated_data):
        products = validated_data.pop('products')
        invoice = Invoice.objects.create(user=self.context['request'].user, **validated_data)
        invoice.products.set(products)
        invoice.calculate_total_amount()
        return invoice