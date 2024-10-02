from rest_framework import status, serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.core.services import OrderService
from rest_framework.decorators import api_view


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, name="", fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name=name, fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


create_order_out_serializer = inline_serializer(name="CreateOrderOutSerializer", fields={
    "order_id": serializers.IntegerField(),
})


@extend_schema(
    tags=["order"],
    request=None,
    responses={"201": create_order_out_serializer},
)
@api_view(["POST"])
def create_order(request):
    order_service = OrderService()
    if request.user.is_authenticated:
        order_service.create_order(request.user)
        return Response({"order_id": order_service.order_id}, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
