from rest_framework import serializers
from products.models import Product
from .models import Invoice

from products.serializers import ProductSerializer

class InvoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    products_info = serializers.SerializerMethodField(read_only=True)
    products = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    status = serializers.CharField(required=False)

    user_id = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['user_id'] = instance.user.id

        return data

    def get_products_info(self, instance) -> ProductSerializer:
        serializer = ProductSerializer(instance.products.all(), many=True)
        return serializer.data

    def create(self, validated_data):
        request = self.context['request'] 
        user = request.user

        product_ids = validated_data.pop('products', [])
        status_value = validated_data.get('status', 'PENDING')

        invoice = Invoice.objects.create(
            user=user,
            status=status_value
        )

        products = Product.objects.filter(id__in=product_ids)
        invoice.products.set(products)
        invoice.calculate_total_amount()
        invoice.save()

        return invoice

    def update(self, instance, validated_data):
        product_ids = validated_data.pop('products', None)
        status_value = validated_data.get('status', None)

        if status_value is not None:
            instance.status = status_value

        if product_ids is not None:
            products = Product.objects.filter(id__in=product_ids)
            instance.products.set(products)
        instance.calculate_total_amount()
        instance.save()
        return instance