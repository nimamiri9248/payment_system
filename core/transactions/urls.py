
from django.urls import path
from .views import (
    TransactionCreateView,
    TransactionListView,
    TransactionDetailView,
)

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),  # new detail route
]
