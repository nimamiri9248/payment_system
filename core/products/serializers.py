from rest_framework import serializers
from .utils import generate_presigned_url
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_signed_image_url(self, obj):
        if not obj.image:
            return None
        return generate_presigned_url(obj.image.name)