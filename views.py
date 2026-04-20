from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import BudgetForm, TransactionForm
from .models import Budget, Transaction
from .services import get_dashboard_data, get_report_data


class DashboardView(ListView):
    model = Transaction
    template_name = 'tracker/dashboard.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.select_related('category')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_dashboard_data())
        return context


class TransactionListView(ListView):
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 12

    def get_queryset(self):
        return Transaction.objects.select_related('category').all()


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def form_valid(self, form):
        messages.success(self.request, 'Операция успешно сохранена.')
        return super().form_valid(form)


class BudgetListView(ListView):
    model = Budget
    template_name = 'tracker/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.select_related('category').all()


class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'tracker/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        messages.success(self.request, 'Лимит бюджета успешно сохранен.')
        return super().form_valid(form)


def report_view(request):
    start_date = request.GET.get('start_date') or None
    end_date = request.GET.get('end_date') or None
    context = get_report_data(start_date, end_date)
    context['start_date'] = start_date or ''
    context['end_date'] = end_date or ''
    return render(request, 'tracker/report.html', context)


def index_redirect(request):
    return redirect('dashboard')
