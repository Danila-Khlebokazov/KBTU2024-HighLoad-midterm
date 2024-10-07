from apps.authentication.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        indexes = [models.Index(fields=["name"], name="category_name_idx")]


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name", "category"], name="product_category_name_idx"),
            models.Index(fields=["price"], name="price_idx"),
        ]


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        FINISHED = "FINISHED", "Finished"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(
        choices=Status.choices, default=Status.CREATED, max_length=10, editable=False
    )

    @property
    def can_add_products(self):
        return self.status == Order.Status.CREATED

    @property
    def products_count(self):
        return self.items.count()

    def __str__(self):
        return f"Order {self.pk}, {self.user.username}, {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["user"], name="user_idx"),
            models.Index(fields=["status"], name="status_idx"),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        indexes = [models.Index(fields=["order", "product"], name="order_product_idx")]
