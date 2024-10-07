from .category_views import CategoriesView
from .order_views import (
    OrderAddProductView,
    OrderCancelView,
    OrderDeliveryView,
    OrderDetailView,
    OrderFinishView,
    OrderPaymentView,
    OrderRemoveAllProductView,
    OrderRemoveProductView,
    OrdersView,
)
from .product_views import ProductsView

__all__ = [
    "OrdersView",
    "OrderDetailView",
    "OrderCancelView",
    "ProductsView",
    "CategoriesView",
    "OrderPaymentView",
    "OrderDeliveryView",
    "OrderFinishView",
    "OrderAddProductView",
    "OrderRemoveProductView",
    "OrderRemoveAllProductView",
]
