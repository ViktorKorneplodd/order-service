Запуск проекта
1. `python -m venv venv`
2. `source venv/bin/activate` (или `venv\Scripts\activate` на Windows)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

Тестирование
`curl -X POST http://127.0.0.1:8000/api/orders/create/ -H "Content-Type: application/json" -d @test.json`
`curl -X POST http://127.0.0.1:8000/api/orders/create/ -H "Content-Type: application/json" -d @test_with_promo.json`


