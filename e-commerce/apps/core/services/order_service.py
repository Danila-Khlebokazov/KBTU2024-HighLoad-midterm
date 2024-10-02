from typing import Optional, overload, Callable, Union, List

from django.contrib.auth.models import User
from multipledispatch import dispatch
from django.shortcuts import get_object_or_404

from constants import CANNOT_ADD_PRODUCT, CANNOT_REMOVE_PRODUCT, WRONG_SEQUENCE, EMPTY_ORDER
from apps.core.models import Order, OrderItem
from exceptions import ServiceException


class OrderService:
    order_objects = Order.objects
    order_item_objects = OrderItem.objects

    def __init__(self, order_id: Optional[int] = None):
        self.order_id = order_id

    # --------- CREATED
    def create_order(self, user: User):
        order = self.order_objects.create(user=user)
        self.order_id = order.id
        return order

    def _calculate_total_price(self, pk: int = None):
        total_price = 0
        if pk is not None:
            items = self.order_item_objects.filter(order_id=self.order_id)
        else:
            items = self.order_item_objects.filter(order_id=pk)
        for item in items:
            total_price += item.product.price * item.quantity
        return total_price

    def get_all_orders(self, user: User):
        return self.order_objects.filter(user=user)

    @overload
    def get_order(self, pk: int = None) -> Order:
        ...

    def get_order(self, pk: int = None) -> Order:
        to_find = self.order_id
        if pk:
            to_find = pk
        # to escape N+1 problem
        return get_object_or_404(
            self.order_objects.select_related("user").prefetch_related("items", "items__product"),
            id=to_find
        )

    @dispatch(int, int)
    def add_products(self, product_id: int, quantity: int = 1) -> None:
        if self.get_order().status != Order.Status.CREATED:
            raise ServiceException(CANNOT_ADD_PRODUCT)
        self.order_item_objects.create(order_id=self.order_id, product_id=product_id, quantity=quantity)
        self._calculate_total_price()

    @dispatch(int, int, int)
    def add_products(self, pk: int, product_id: int, quantity: int = 1) -> None:
        if self.get_order(pk).status != Order.Status.CREATED:
            raise ServiceException(CANNOT_ADD_PRODUCT)
        self.order_item_objects.create(order_id=pk, product_id=product_id, quantity=quantity)
        self._calculate_total_price(pk)

    @dispatch(int, int)
    def remove_products(self, product_id: int, quantity: int = 1) -> None:
        if self.get_order().status != Order.Status.CREATED:
            raise ServiceException(CANNOT_REMOVE_PRODUCT)

        items = self.order_item_objects.filter(order_id=self.order_id, product_id=product_id).first()
        if items:
            if items.quantity <= quantity:
                items.delete()
            else:
                items.quantity -= quantity
                items.save()
            self._calculate_total_price()

    @dispatch(int, int, int)
    def remove_products(self, pk: int, product_id: int, quantity: int = 1) -> None:
        if self.get_order().status != Order.Status.CREATED:
            raise ServiceException(CANNOT_REMOVE_PRODUCT)

        items = self.order_item_objects.filter(order_id=pk, product_id=product_id).first()
        if items:
            if items.quantity <= quantity:
                items.delete()
            else:
                items.quantity -= quantity
                items.save()
            self._calculate_total_price(pk)

    def _change_status(
        self,
        old_status: Union[Order.Status, List[Order.Status]],
        new_status: Order.Status,
        pk: int = None,
        exec_after_validation: Callable = lambda _: None,
        exec_after_saving: Callable = lambda _: None,
    ):
        if pk:
            order = self.get_order(pk)
        else:
            order = self.get_order()
        if isinstance(old_status, list):
            if order.status not in old_status:
                raise ServiceException(WRONG_SEQUENCE)
        elif isinstance(old_status, Order.Status):
            if order.status != old_status:
                raise ServiceException(WRONG_SEQUENCE)
        else:
            raise ValueError("Old status must be Order.Status or List[Order.Status]")
        exec_after_validation(order)
        order.status = new_status
        order.save()
        exec_after_saving(order)

    # ------------- PAYED
    def payment_release(self, pk: int = None):
        def paying_validation(order: Order):
            if order.total_price == 0:
                raise ServiceException(EMPTY_ORDER)

        self._change_status(
            Order.Status.CREATED,
            Order.Status.PAID,
            pk,
            exec_after_validation=paying_validation
        )

    # ------------- SHIPPED
    def delivery_release(self, pk: int = None):
        self._change_status(
            Order.Status.PAID,
            Order.Status.SHIPPED,
            pk,
        )

    # ------------- FINISHED
    def finishing(self, pk: int = None):
        self._change_status(
            Order.Status.SHIPPED,
            Order.Status.FINISHED,
            pk,
        )

    # ------------- CANCELLED
    def cancel(self, pk: int = None):
        self._change_status(
            [Order.Status.CREATED, Order.Status.PAID, Order.Status.SHIPPED],
            Order.Status.CANCELLED,
            pk,
        )
