from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Invoice
from .serializers import InvoiceSerializer
from .permissions import IsOwnerOrAdmin

class InvoiceListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get(self, request):
        if request.user.is_staff:
            invoices = Invoice.objects.all()
        else:
            invoices = Invoice.objects.filter(user=request.user)
        serializer = self.serializer_class(invoices, many=True, context={'request': request})
        return Response(
            {
                "message": "Invoices retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            invoice = serializer.save()
            return Response(
                {
                    "message": "Invoice created successfully.",
                    "result": self.serializer_class(invoice, context={'request': request}).data
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

class InvoiceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = InvoiceSerializer
    def get_object(self, pk):
        return get_object_or_404(Invoice, pk=pk)
    
    def get(self, request, pk):
        invoice = self.get_object(pk)
        self.check_object_permissions(request, invoice)
        serializer = self.serializer_class(invoice, context={'request': request})
        return Response(
            {
                "message": "Invoice retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
