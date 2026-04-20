from django.urls import path

from .views import (
    BudgetCreateView,
    BudgetListView,
    DashboardView,
    TransactionCreateView,
    TransactionListView,
    index_redirect,
    report_view,
)

urlpatterns = [
    path('', index_redirect, name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', TransactionCreateView.as_view(), name='transaction-add'),
    path('reports/', report_view, name='reports'),
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budgets/add/', BudgetCreateView.as_view(), name='budget-add'),
]
