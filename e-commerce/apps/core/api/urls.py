from apps.core.api.views import (
    CategoriesView,
    OrderCancelView,
    OrderDetailView,
    OrdersView,
    ProductsView,
)
from django.urls import path

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="create_order"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="get_orders"),
    path("orders/<int:pk>/cancel", OrderCancelView.as_view(), name="cancel_orders"),
    path("products/", ProductsView.as_view(), name="list_products"),
    path("categories/", CategoriesView.as_view(), name="list_categories"),
]
