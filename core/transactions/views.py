from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Transaction
from .serializers import TransactionCreateSerializer, TransactionListSerializer

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

    def get(self, request):
        user = request.user
        if user.is_staff:
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(invoice__user=user)
        serializer = TransactionListSerializer(transactions, many=True)
        return Response(
            {
                "message": "Transaction history retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )
