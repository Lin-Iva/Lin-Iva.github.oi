from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    CATEGORY_TYPES = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]

    name = models.CharField('Название', max_length=120)
    category_type = models.CharField('Тип', max_length=10, choices=CATEGORY_TYPES)
    color = models.CharField('Цвет', max_length=7, default='#4f46e5')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category_type', 'name']
        unique_together = ('name', 'category_type')

    def __str__(self):
        return f'{self.name} ({self.get_category_type_display()})'


class Transaction(models.Model):
    INCOME = Category.INCOME
    EXPENSE = Category.EXPENSE
    TRANSACTION_TYPES = Category.CATEGORY_TYPES

    title = models.CharField('Операция', max_length=150)
    transaction_type = models.CharField('Тип', max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_date = models.DateField('Дата операции', default=timezone.localdate)
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
        ordering = ['-transaction_date', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.amount}'

    def clean(self):
        if self.category and self.category.category_type != self.transaction_type:
            from django.core.exceptions import ValidationError

            raise ValidationError({'category': 'Тип категории должен совпадать с типом операции.'})


class Budget(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория расходов',
        on_delete=models.CASCADE,
        limit_choices_to={'category_type': Category.EXPENSE},
        related_name='budgets',
    )
    month = models.DateField('Месяц')
    limit_amount = models.DecimalField('Лимит', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Бюджет'
        verbose_name_plural = 'Бюджеты'
        ordering = ['-month', 'category__name']
        unique_together = ('category', 'month')

    def __str__(self):
        return f'{self.category.name} - {self.month:%m.%Y}'

    @property
    def spent_amount(self):
        start = self.month.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        total = self.category.transactions.filter(
            transaction_type=Category.EXPENSE,
            transaction_date__gte=start,
            transaction_date__lt=end,
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        return total

    @property
    def usage_percent(self):
        if not self.limit_amount:
            return 0
        return round(float((self.spent_amount / self.limit_amount) * 100), 1)
