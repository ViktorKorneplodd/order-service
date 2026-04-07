from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Good(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    excluded_from_promotions = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    valid_until = models.DateTimeField()
    max_usages = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    applicable_category = models.CharField(max_length=100, blank=True, null=True)

    def is_valid(self):
        return self.valid_until > timezone.now() and self.used_count < self.max_usages

    def __str__(self):
        return self.code


class Order(models.Model):
    user_id = models.PositiveIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by user {self.user_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    good = models.ForeignKey(Good, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def total(self):
        return self.price_at_order * self.quantity * (1 - self.discount_percent / 100)