from apps.core.models import Category
from apps.core.serializers import CategorySerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny


@extend_schema(tags=["categories"], summary="Get all categories.")
class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
