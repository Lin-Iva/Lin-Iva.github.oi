from django.contrib import admin

from .models import Budget, Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'color')
    list_filter = ('category_type',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'transaction_type', 'category', 'amount', 'transaction_date')
    list_filter = ('transaction_type', 'category', 'transaction_date')
    search_fields = ('title', 'comment')


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'month', 'limit_amount')
    list_filter = ('month', 'category')
