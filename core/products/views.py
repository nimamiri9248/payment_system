from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema

class ProductListCreateView(APIView):
    """
    GET: List all products.
    POST: Create a new product (admin only).
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    
    @extend_schema(
        operation_id="productsListGet"
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True, context={'request': request})
        return Response(
            {
                "message": "Products retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {
                    "message": "Product created successfully.",
                    "result": self.serializer_class(product, context={'request': request}).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Validation error.",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ProductDetailView(APIView):
    """
    GET: Retrieve a specific product.
    PUT: Update a specific product (admin only).
    PATCH: Partially update a specific product (admin only).
    DELETE: Delete a specific product (admin only).
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @extend_schema(
        operation_id="productGet"
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {
                    "message": "Product not found.",
                    "result": {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(product, context={'request': request})
        return Response(
            {
                "message": "Product retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {
                    "message": "Product not found.",
                    "result": {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {
                    "message": "Product updated successfully.",
                    "result": self.serializer_class(product, context={'request': request}).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Validation error.",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {
                    "message": "Product not found.",
                    "result": {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(product, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                {
                    "message": "Product updated successfully.",
                    "result": self.serializer_class(product, context={'request': request}).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Validation error.",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {
                    "message": "Product not found.",
                    "result": {}
                },
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(
            {
                "message": "Product deleted successfully.",
                "result": {}
            },
            status=status.HTTP_204_NO_CONTENT
        )
