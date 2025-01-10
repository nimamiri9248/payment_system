from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Transaction
from .serializers import TransactionCreateSerializer, TransactionListSerializer, TransactionStatusUpdateSerializer

class TransactionCreateView(APIView):
    """
    POST: Register a transaction for an invoice.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            transaction = serializer.save()
            response_serializer = TransactionListSerializer(transaction)
            return Response(
                {
                    "message": "Transaction registered successfully.",
                    "result": response_serializer.data
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

class TransactionListView(APIView):
    """
    GET: View transaction history.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionListSerializer

    def get(self, request):
        user = request.user
        if user.is_staff:
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(invoice__user=user)
        serializer = self.serializer_class(transactions, many=True)
        return Response(
            {
                "message": "Transaction history retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )

class TransactionDetailView(APIView):
    """
    GET: Retrieve one transaction item by ID.
    PUT: Full update of a transaction.
    PATCH: Partial update of a transaction.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionStatusUpdateSerializer

    def get_object(self, pk, user):
        transaction = get_object_or_404(Transaction, pk=pk)
        if not user.is_staff and transaction.invoice.user != user:
            return None 
        return transaction

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response(
                {"message": "You do not have permission to view this transaction.", "result": {}},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TransactionListSerializer(transaction)
        return Response(
            {
                "message": "Transaction retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )


    def patch(self, request, pk):
        """
        Partial update: only the status field will be updated.
        """
        transaction = self.get_object(pk, request.user)
        if not transaction:
            return Response(
                {"message": "You do not have permission to update this transaction.", "result": {}},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.serializer_class(
            transaction,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            transaction = serializer.save()
            response_serializer = TransactionListSerializer(transaction)
            return Response(
                {
                    "message": "Transaction updated successfully (partial).",
                    "result": response_serializer.data
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

