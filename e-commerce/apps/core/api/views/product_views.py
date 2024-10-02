from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from apps.core.models import Product
from apps.core.serializers import ProductSerializer


@extend_schema(
    tags=["products"],
    summary="Get all products."
)
class ProductsView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = ProductSerializer
