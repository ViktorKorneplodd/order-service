# Order Service with Promo Codes

Сервис для создания заказов с поддержкой промокодов на Django REST Framework.

## Функциональность

- Создание заказа с товарами
- Применение промокодов со скидкой
- Валидация промокодов:
  - Проверка срока действия
  - Лимит использований
  - Одноразовость на пользователя
  - Фильтр по категориям товаров
  - Исключение некоторых товаров из акций

## Запуск проекта
1. `python -m venv venv`
2. `source venv/bin/activate` (или `venv\Scripts\activate` на Windows)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

## Как тестировать API

## Откройте терминал и выполните:
`python manage.py shell`

### Подготовка тестовых данных

## Откройте терминал и выполните:
from orders.models import Good, PromoCode
from django.utils import timezone
from datetime import timedelta

Good.objects.create(id=1, name="Ноутбук", price=1000, category="electronics")
Good.objects.create(id=2, name="Мышь", price=50, category="electronics", excluded_from_promotions=True)
Good.objects.create(id=3, name="Книга", price=30, category="books")
PromoCode.objects.create(
    code="SUMMER2025",
    discount_percent=10,
    valid_until=timezone.now() + timedelta(days=30),
    max_usages=5,
    applicable_category="electronics"
)
print("Готово!")
exit()

## Отправьте тестовый запрос
`curl -X POST http://127.0.0.1:8000/api/orders/create/ -H "Content-Type: application/json" -d "{\"user_id\":1,\"goods\":[{\"good_id\":1,\"quantity\":2}],\"promo_code\":\"SUMMER2025\"}"`
## Для Linux/macOS
`curl -X POST http://127.0.0.1:8000/api/orders/create/ -H "Content-Type: application/json" -d '{"user_id":1,"goods":[{"good_id":1,"quantity":2}],"promo_code":"SUMMER2025"}'`

## Другие тесты
- Заказ без промокода	   | {"user_id":2,"goods":[{"good_id":3,"quantity":1}]} |
- Неверный промокод	       | {"user_id":3,"goods":[{"good_id":1,"quantity":1}],"promo_code":"FAKE"} |
- Товар исключён из акций	| {"user_id":4,"goods":[{"good_id":2,"quantity":1}],"promo_code":"SUMMER2025"} |
