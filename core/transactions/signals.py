from django.db.models.signals import post_save
from django.dispatch import receiver
from transactions.models import Transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Transaction)
def transaction_status_notification(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    user_id = instance.invoice.user.id
    group_name = f'user_{user_id}_transactions'
    message = {
        "transaction_id": instance.id,
        "invoice_id": instance.invoice.id,
        "amount": str(instance.amount),
        "status": instance.status,
        "transaction_date": str(instance.transaction_date),
    }
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "transaction_update",
            "message": message,
        }
    )