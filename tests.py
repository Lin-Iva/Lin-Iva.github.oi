from django.test import TestCase
from django.urls import reverse

from .models import Category, Transaction


class TrackerViewsTest(TestCase):
    def setUp(self):
        self.salary = Category.objects.create(name='Зарплата', category_type='income')
        self.food = Category.objects.create(name='Продукты', category_type='expense')
        Transaction.objects.create(title='Аванс', transaction_type='income', category=self.salary, amount=50000)
        Transaction.objects.create(title='Супермаркет', transaction_type='expense', category=self.food, amount=5200)

    def test_dashboard_page(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Финансовая панель')

    def test_reports_page(self):
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Отчеты по категориям')
