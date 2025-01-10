from django.urls import re_path
from transactions.consumers import UserTransactionConsumer

websocket_urlpatterns = [
    re_path(r'ws/transactions/user/(?P<user_id>\d+)/$', UserTransactionConsumer.as_asgi()),
]