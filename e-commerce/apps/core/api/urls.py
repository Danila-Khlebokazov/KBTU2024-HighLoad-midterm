from apps.core.api.views import (
    CategoriesView,
    OrderAddProductView,
    OrderCancelView,
    OrderDeliveryView,
    OrderDetailView,
    OrderFinishView,
    OrderPaymentView,
    OrderRemoveAllProductView,
    OrderRemoveProductView,
    OrdersView,
    ProductsView,
)
from django.urls import path

urlpatterns = [
    path("orders/", OrdersView.as_view(), name="create_order"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="get_orders"),
    path("orders/<int:pk>/add", OrderAddProductView.as_view(), name="add_product_orders"),
    path("orders/<int:pk>/remove", OrderRemoveProductView.as_view(), name="remove_product_orders"),
    path(
        "orders/<int:pk>/remove-all",
        OrderRemoveAllProductView.as_view(),
        name="remove_all_product_orders",
    ),
    path("orders/<int:pk>/payment", OrderPaymentView.as_view(), name="payment_orders"),
    path("orders/<int:pk>/delivery", OrderDeliveryView.as_view(), name="delivery_orders"),
    path("orders/<int:pk>/finish", OrderFinishView.as_view(), name="finish_orders"),
    path("orders/<int:pk>/cancel", OrderCancelView.as_view(), name="cancel_orders"),
    path("products/", ProductsView.as_view(), name="list_products"),
    path("categories/", CategoriesView.as_view(), name="list_categories"),
]
