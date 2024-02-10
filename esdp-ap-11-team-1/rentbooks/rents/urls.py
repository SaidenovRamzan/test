from django.urls import path
from rents.views import (
    OrderDetailView, UserShelfDetailView
)

urlpatterns = [
    path('user_shelf/<int:pk>/detail/', UserShelfDetailView.as_view(), name='user_shelf_detail'),
    path('orders/<int:pk>/detail', OrderDetailView.as_view(), name='order_detail'),
]
