from django.utils import timezone
from .models import PromoCode, Good

def validate_promo_code(promo_code_str, user_id, goods_data):
    try:
        promo = PromoCode.objects.get(code=promo_code_str)
    except PromoCode.DoesNotExist:
        return None, "Промокод не существует"

    if promo.valid_until <= timezone.now():
        return None, "Промокод просрочен"
    if promo.used_count >= promo.max_usages:
        return None, "Промокод достиг лимита использований"

    from .models import Order
    if Order.objects.filter(user_id=user_id, promo_code=promo).exists():
        return None, "Вы уже использовали этот промокод"

    good_ids = [item['good_id'] for item in goods_data]
    goods = Good.objects.filter(id__in=good_ids)

    if goods.filter(excluded_from_promotions=True).exists():
        return None, "В заказе есть товары, исключённые из акций"

    if promo.applicable_category:
        if goods.exclude(category=promo.applicable_category).exists():
            return None, f"Промокод действует только на категорию {promo.applicable_category}"

    return promo, None