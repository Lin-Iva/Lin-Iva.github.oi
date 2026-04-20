import base64
from io import BytesIO
from typing import Iterable

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db.models import Sum

from .models import Budget, Category, Transaction


plt.rcParams['font.family'] = 'DejaVu Sans'


def money(value):
    return f'{value:,.2f}'.replace(',', ' ')


def chart_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=140)
    plt.close(fig)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def build_category_pie(queryset: Iterable[Transaction], title: str):
    data = (
        queryset.filter(transaction_type=Transaction.EXPENSE)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    labels = [row['category__name'] for row in data]
    values = [float(row['total']) for row in data]
    if not values:
        return None
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.pie(values, labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops={'width': 0.45})
    ax.set_title(title)
    return chart_to_base64(fig)


def build_income_expense_bar(queryset: Iterable[Transaction], title: str):
    income = queryset.filter(transaction_type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
    expense = queryset.filter(transaction_type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.bar(['Доходы', 'Расходы'], [float(income), float(expense)])
    ax.set_title(title)
    ax.set_ylabel('Сумма, ₽')
    ax.grid(axis='y', alpha=0.25)
    return chart_to_base64(fig)


def build_budget_progress(budgets: Iterable[Budget]):
    labels = [budget.category.name for budget in budgets]
    values = [min(float(budget.usage_percent), 150.0) for budget in budgets]
    if not values:
        return None
    fig, ax = plt.subplots(figsize=(6.2, 3.5))
    ax.barh(labels, values)
    ax.set_xlim(0, 150)
    ax.set_xlabel('% использования лимита')
    ax.set_title('Контроль бюджета по категориям')
    ax.grid(axis='x', alpha=0.25)
    return chart_to_base64(fig)


def get_dashboard_data():
    transactions = Transaction.objects.select_related('category')
    total_income = transactions.filter(transaction_type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(transaction_type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    latest_transactions = transactions[:8]
    expense_breakdown = (
        transactions.filter(transaction_type=Transaction.EXPENSE)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')[:5]
    )
    active_budgets = list(Budget.objects.select_related('category')[:5])
    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'latest_transactions': latest_transactions,
        'expense_breakdown': expense_breakdown,
        'budgets': active_budgets,
        'expense_chart': build_category_pie(transactions, 'Структура расходов'),
        'balance_chart': build_income_expense_bar(transactions, 'Доходы и расходы'),
        'budget_chart': build_budget_progress(active_budgets),
    }


def get_report_data(start_date=None, end_date=None):
    queryset = Transaction.objects.select_related('category')
    if start_date:
        queryset = queryset.filter(transaction_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(transaction_date__lte=end_date)

    income_by_category = queryset.filter(transaction_type=Transaction.INCOME).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    expense_by_category = queryset.filter(transaction_type=Transaction.EXPENSE).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    return {
        'transactions': queryset,
        'income_by_category': income_by_category,
        'expense_by_category': expense_by_category,
        'expense_chart': build_category_pie(queryset, 'Расходы по категориям'),
        'balance_chart': build_income_expense_bar(queryset, 'Сравнение доходов и расходов'),
    }
