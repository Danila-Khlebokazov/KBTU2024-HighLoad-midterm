from apps.core.serializers import (
    FullOrderSerializer,
    SimpleOrderSerializer,
    create_order_out_serializer,
)
from apps.core.services import OrderService
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema(
    tags=["orders"],
)
class OrdersView(APIView):
    permission_classes = [IsAuthenticated]
    get_serializer_class = SimpleOrderSerializer

    @extend_schema(
        request=None,
        responses={status.HTTP_200_OK: get_serializer_class},
        summary="Get all user orders.",
    )
    def get(self, request):
        order_service = OrderService()
        orders = order_service.get_all_orders(request.user)
        serializer = self.get_serializer_class(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None, responses={"201": create_order_out_serializer}, summary="Create a new order."
    )
    def post(self, request):
        order_service: OrderService = OrderService()
        order_service.create_order(request.user)
        return Response({"order_id": order_service.order.id}, status=status.HTTP_201_CREATED)


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
        operation_id="api_core_orders_details_retrieve",
    )
    def get(self, request, pk):
        order_service = OrderService(pk)
        order = order_service.get_order()
        serializer = self.get_serializer_class(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["orders"], summary="Add product to order.")
class OrderAddProductView(APIView):
    permission_classes = [IsAuthenticated]

    class AddProductSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField(default=1)

    @extend_schema(
        request=AddProductSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        serializer = self.AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_service = OrderService(pk)
        order_service.add_products(**serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Remove product from order.")
class OrderRemoveProductView(APIView):
    permission_classes = [IsAuthenticated]

    class RemoveProductSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField(default=1)

    @extend_schema(
        request=RemoveProductSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        serializer = self.RemoveProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_service = OrderService(pk)
        order_service.remove_products(**serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Remove all products from order.")
class OrderRemoveAllProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        order_service = OrderService(pk)
        order_service.remove_all_products()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Switch to payment of order.")
class OrderPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        order_service = OrderService(pk)
        order_service.payment_release()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Switch to delivery of order.")
class OrderDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        order_service = OrderService(pk)
        order_service.delivery_release()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Finish an order.")
class OrderFinishView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, pk):
        order_service = OrderService(pk)
        order_service.finishing()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["orders"], summary="Cancel an order.")
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
