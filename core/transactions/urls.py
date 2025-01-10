from django.urls import path
from .views import TransactionCreateView, TransactionListView

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('', TransactionListView.as_view(), name='transaction-list'),
]
