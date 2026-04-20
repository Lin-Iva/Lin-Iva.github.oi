from decimal import Decimal
from datetime import date

from django.core.management.base import BaseCommand

from tracker.models import Budget, Category, Transaction


class Command(BaseCommand):
    help = 'Заполняет демонстрационными данными систему учета финансов.'

    def handle(self, *args, **options):
        categories = {
            ('Зарплата', 'income'): '#16a34a',
            ('Фриланс', 'income'): '#0ea5e9',
            ('Инвестиции', 'income'): '#8b5cf6',
            ('Продукты', 'expense'): '#ef4444',
            ('Транспорт', 'expense'): '#f97316',
            ('Жилье', 'expense'): '#f59e0b',
            ('Развлечения', 'expense'): '#6366f1',
            ('Здоровье', 'expense'): '#14b8a6',
        }
        category_objects = {}
        for (name, category_type), color in categories.items():
            category_objects[(name, category_type)], _ = Category.objects.get_or_create(
                name=name, category_type=category_type, defaults={'color': color}
            )

        if Transaction.objects.exists():
            self.stdout.write(self.style.WARNING('Данные уже существуют.'))
            return

        transactions = [
            ('Зарплата за месяц', 'income', 'Зарплата', Decimal('120000.00'), date(2026, 4, 1), 'Основной доход'),
            ('Проект для клиента', 'income', 'Фриланс', Decimal('35000.00'), date(2026, 4, 5), 'Лендинг для заказчика'),
            ('Купоны брокера', 'income', 'Инвестиции', Decimal('8000.00'), date(2026, 4, 7), 'Доход по облигациям'),
            ('Супермаркет', 'expense', 'Продукты', Decimal('12450.00'), date(2026, 4, 2), 'Покупки на неделю'),
            ('Метро и такси', 'expense', 'Транспорт', Decimal('4600.00'), date(2026, 4, 3), 'Поездки по городу'),
            ('Аренда квартиры', 'expense', 'Жилье', Decimal('42000.00'), date(2026, 4, 4), 'Ежемесячный платеж'),
            ('Кино и кафе', 'expense', 'Развлечения', Decimal('6900.00'), date(2026, 4, 9), 'Выходные'),
            ('Аптека', 'expense', 'Здоровье', Decimal('2300.00'), date(2026, 4, 11), 'Лекарства'),
            ('Супермаркет', 'expense', 'Продукты', Decimal('9150.00'), date(2026, 4, 12), 'Покупки для дома'),
            ('Транспортная карта', 'expense', 'Транспорт', Decimal('2500.00'), date(2026, 4, 13), 'Пополнение карты'),
        ]
        for title, transaction_type, category_name, amount, transaction_date, comment in transactions:
            Transaction.objects.create(
                title=title,
                transaction_type=transaction_type,
                category=category_objects[(category_name, transaction_type)],
                amount=amount,
                transaction_date=transaction_date,
                comment=comment,
            )

        month = date(2026, 4, 1)
        budget_rows = [
            ('Продукты', Decimal('25000.00')),
            ('Транспорт', Decimal('8000.00')),
            ('Жилье', Decimal('45000.00')),
            ('Развлечения', Decimal('12000.00')),
            ('Здоровье', Decimal('5000.00')),
        ]
        for category_name, limit_amount in budget_rows:
            Budget.objects.create(
                category=category_objects[(category_name, 'expense')],
                month=month,
                limit_amount=limit_amount,
            )

        self.stdout.write(self.style.SUCCESS('Демонстрационные данные загружены.'))
