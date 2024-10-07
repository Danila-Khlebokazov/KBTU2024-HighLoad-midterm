from typing import Callable, List, Optional, Union

from apps.core.models import Order, OrderItem
from apps.core.tasks import send_sms_to_user
from constants import CANNOT_ADD_PRODUCT, CANNOT_REMOVE_PRODUCT, EMPTY_ORDER, WRONG_SEQUENCE
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from exceptions import ServiceException


class OrderService:
    order_objects: Order.objects = Order.objects
    order_item_objects: OrderItem.objects = OrderItem.objects
    order: Optional[Order] = None

    def __init__(self, order_id: Optional[int] = None):
        if order_id:
            self.order = get_object_or_404(
                self.order_objects.select_related("user").prefetch_related(
                    Prefetch("items", queryset=self.order_item_objects.select_related("product"))
                ),
                id=order_id,
            )

    # --------- CREATED
    def create_order(self, user: User) -> Order:
        order = self.order_objects.create(user=user)
        self.order = order
        return order

    def get_order(self) -> Order:
        return self.order

    def get_all_orders(self, user: User):
        return self.order_objects.filter(user=user)

    def add_products(self, product_id: int, quantity: int = 1) -> None:
        if self.order.status != Order.Status.CREATED:
            raise ServiceException(CANNOT_ADD_PRODUCT)

        if (
            item := self.order_item_objects.filter(order_id=self.order.id, product_id=product_id)
            .select_related("product")
            .first()
        ):
            item.quantity += quantity
            item.save()
        else:
            item = self.order_item_objects.create(
                order_id=self.order.id, product_id=product_id, quantity=quantity
            )

        added_price = item.product.price * quantity
        self.order.total_price += added_price
        self.order.save()

    def remove_products(self, product_id: int, quantity: int = 1) -> None:
        if self.order.status != Order.Status.CREATED:
            raise ServiceException(CANNOT_REMOVE_PRODUCT)

        if (
            items := self.order_item_objects.filter(order_id=self.order.id, product_id=product_id)
            .select_related("product")
            .first()
        ):
            if items.quantity <= quantity:
                quantity = items.quantity
                items.delete()
            else:
                items.quantity -= quantity
                items.save()

            removed_price = items.product.price * quantity
            self.order.total_price += removed_price
            self.order.save()

    def remove_all_products(self) -> None:
        items = self.order_item_objects.filter(order_id=self.order.id)
        items.delete()
        self.order.total_price = 0
        self.order.save()

    def _change_status(
        self,
        old_status: Union[Order.Status, List[Order.Status]],
        new_status: Order.Status,
        exec_after_validation: Callable = lambda _: None,
        exec_after_saving: Callable = lambda _: None,
    ) -> None:
        if isinstance(old_status, list):
            if self.order.status not in old_status:
                raise ServiceException(WRONG_SEQUENCE)
        elif isinstance(old_status, Order.Status):
            if self.order.status != old_status:
                raise ServiceException(WRONG_SEQUENCE)
        else:
            raise ValueError("Old status must be Order.Status or List[Order.Status]")
        exec_after_validation(self.order)
        self.order.status = new_status
        self.order.save()
        exec_after_saving(self.order)

    # ------------- PAYED
    def payment_release(self) -> None:
        def paying_validation(order: Order):
            if order.total_price == 0:
                raise ServiceException(EMPTY_ORDER)

        message = "Your order {order_id} is packed, please pay to get it.".format(
            order_id=self.order.id
        )
        self._change_status(
            Order.Status.CREATED,
            Order.Status.PAID,
            exec_after_validation=paying_validation,
        )
        send_sms_to_user(message=message, user=self.order.user)

    # ------------- SHIPPED
    def delivery_release(self):
        message = "Your order {order_id} is payed, wait for delivering.".format(
            order_id=self.order.id
        )
        self._change_status(
            Order.Status.PAID,
            Order.Status.SHIPPED,
        )
        send_sms_to_user(message=message, user=self.order.user)

    # ------------- FINISHED
    def finishing(self):
        message = "Thank you for purchasing order {order_id}!".format(order_id=self.order.id)
        self._change_status(
            Order.Status.SHIPPED,
            Order.Status.FINISHED,
        )
        send_sms_to_user(message=message, user=self.order.user)

    # ------------- CANCELLED
    def cancel(self):
        message = "Your order {order_id} is canceled!".format(order_id=self.order.id)
        self._change_status(
            [Order.Status.CREATED, Order.Status.PAID, Order.Status.SHIPPED],
            Order.Status.CANCELLED,
        )
        send_sms_to_user(message=message, user=self.order.user)
