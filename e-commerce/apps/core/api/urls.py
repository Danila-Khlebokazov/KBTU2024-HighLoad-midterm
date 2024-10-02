from django.urls import path
from apps.core.api.views import (
    OrdersView,
    OrderDetailView,
    OrderCancelView
)

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="create_order"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="get_orders"),
    path("orders/<int:pk>/cancel", OrderCancelView.as_view(), name="cancel_orders"),
]
