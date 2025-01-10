from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'status', 'transaction_date')
    search_fields = ('invoice__id', 'invoice__user__username', 'status')
    list_filter = ('status', 'transaction_date')
    ordering = ('-transaction_date',)
