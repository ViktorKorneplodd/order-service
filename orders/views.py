from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from decimal import Decimal
from .models import Good, Order, OrderItem, PromoCode
from .serializers import OrderCreateSerializer, OrderResponseSerializer, OrderItemOutputSerializer
from .services import validate_promo_code

class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user_id = data['user_id']
        goods_data = data['goods']
        promo_code_str = data.get('promo_code')

        good_ids = [item['good_id'] for item in goods_data]
        goods_db = {g.id: g for g in Good.objects.filter(id__in=good_ids)}

        missing = set(good_ids) - set(goods_db.keys())
        if missing:
            return Response({"error": f"Товары не найдены: {missing}"}, status=400)

        total_price = Decimal('0')
        items_info = []
        for item in goods_data:
            good = goods_db[item['good_id']]
            price = good.price
            qty = item['quantity']
            subtotal = price * qty
            total_price += subtotal
            items_info.append({
                'good': good,
                'quantity': qty,
                'price_at_order': price,
                'discount_percent': Decimal('0')
            })

        discount = Decimal('0')
        promo = None

        if promo_code_str:
            promo, error = validate_promo_code(promo_code_str, user_id, goods_data)
            if error:
                return Response({"error": error}, status=400)
            discount = promo.discount_percent
            for item in items_info:
                item['discount_percent'] = discount

        final_total = total_price * (1 - discount / 100)

        with transaction.atomic():
            order = Order.objects.create(user_id=user_id, promo_code=promo)
            order_items = []
            for item in items_info:
                order_items.append(OrderItem(
                    order=order,
                    good=item['good'],
                    quantity=item['quantity'],
                    price_at_order=item['price_at_order'],
                    discount_percent=item['discount_percent']
                ))
            OrderItem.objects.bulk_create(order_items)

            if promo:
                promo.used_count += 1
                promo.save(update_fields=['used_count'])

        output_items = []
        for item in order_items:
            output_items.append({
                'good_id': item.good.id,
                'quantity': item.quantity,
                'price': item.price_at_order,
                'discount': item.discount_percent,
                'total': item.total
            })

        response_data = {
            'user_id': order.user_id,
            'order_id': order.id,
            'goods': output_items,
            'price': total_price,
            'discount': discount,
            'total': final_total
        }
        return Response(response_data, status=status.HTTP_201_CREATED)