from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'products__name')
    list_filter = ('status', 'created_at', 'updated_at')
    filter_horizontal = ('products',)
