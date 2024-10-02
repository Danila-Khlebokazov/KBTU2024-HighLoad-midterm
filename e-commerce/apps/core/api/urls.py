
from django.urls import path
from apps.core.api.views import (
    create_order
)

urlpatterns = [
    path("orders/", create_order, name="create_order"),
]