from apps.core.models import Category, Order, OrderItem, Product
from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, name="", fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name=name, fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


create_order_out_serializer = inline_serializer(
    name="CreateOrderOutSerializer",
    fields={
        "order_id": serializers.IntegerField(),
    },
)


class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ("user",)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class FullOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "updated_at", "total_price", "status", "items")
