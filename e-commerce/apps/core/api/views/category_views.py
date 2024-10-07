from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator

from apps.core.models import Category
from apps.core.serializers import CategorySerializer


@extend_schema(
    tags=["categories"],
    summary="Get all categories."
)
@method_decorator(cache_page(24 * 60 * 60))
class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
