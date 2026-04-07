from rest_framework import serializers
from .models import Order, OrderItem, Good

class OrderItemInputSerializer(serializers.Serializer):
    good_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    goods = OrderItemInputSerializer(many=True)
    promo_code = serializers.CharField(required=False, allow_null=True)

class OrderItemOutputSerializer(serializers.ModelSerializer):
    good_id = serializers.IntegerField(source='good.id')
    price = serializers.DecimalField(source='price_at_order', max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(source='discount_percent', max_digits=5, decimal_places=2)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['good_id', 'quantity', 'price', 'discount', 'total']

class OrderResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    goods = OrderItemOutputSerializer(many=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)