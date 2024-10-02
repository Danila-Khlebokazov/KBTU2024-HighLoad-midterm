from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.serializers import create_order_out_serializer, SimpleOrderSerializer, FullOrderSerializer
from apps.core.services import OrderService


@extend_schema(
    tags=["orders"],
)
class OrdersView(APIView):
    permission_classes = [IsAuthenticated]
    get_serializer_class = SimpleOrderSerializer

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: get_serializer_class},
        summary="Get all user orders."
    )
    def get(self, request):
        order_service = OrderService()
        orders = order_service.get_all_orders(request.user)
        serializer = self.get_serializer_class(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={"201": create_order_out_serializer},
        summary="Create a new order."
    )
    def post(self, request):
        order_service = OrderService()
        order_service.create_order(request.user)
        return Response({"order_id": order_service.order_id}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["orders"],
)
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    get_serializer_class = FullOrderSerializer

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: get_serializer_class},
        summary="Get order details.",
        operation_id="api_core_orders_details_retrieve"
    )
    def get(self, request, pk):
        order_service = OrderService(pk)
        order = order_service.get_order()
        serializer = self.get_serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["orders"],
    summary="Cancel an order."
)
class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def put(self, request, pk):
        order_service = OrderService(pk)
        order_service.cancel()
        return Response(status=status.HTTP_204_NO_CONTENT)
