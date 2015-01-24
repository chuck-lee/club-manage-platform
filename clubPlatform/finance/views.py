from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from datetime import datetime
from finance.models import *
from finance.forms import *


# Create your views here.
def index(request):
    return render(request, 'finance/index.html')

def budgetIndex(request):
    budgets = Budget.objects.order_by('year')

    years = []
    for budget in budgets:
        if budget.year in years:
            continue
        years.append(budget.year)

    context = {
        'years': years
    }
    return render(request, 'finance/budget/index.html', context)

def budget(request, year):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type', 'category')
    budgetList = []
    for budget in budgets:
        budget_last_year = Budget.objects.filter(
            year = int(year) - 1,
            type = budget.type,
            category = budget.category,
            subCategory = budget.subCategory
        ).aggregate(amount=Sum('amount'))

        transaction_last_year = Transaction.objects.filter(
            date__year = int(year) - 1,
            type = budget.type,
            category = budget.category,
            subCategory = budget.subCategory
        ).aggregate(amount=Sum('amount'))

        budgetList.append({
            'id': budget.id,
            'type': '歲入' if budget.type == 1 else '歲出',
            'category': budget.category.name,
            'subCategory': budget.subCategory.name if budget.subCategory != None else '',
            'amount': budget.amount,
            'last_transaction': transaction_last_year['amount'] if transaction_last_year['amount'] != None else 0,
            'last_budget': budget_last_year['amount'] if budget_last_year['amount'] != None else 0,
        })

    context = {
        'year': year,
        'budgetList': budgetList,
    }
    return render(request, 'finance/budget/table.html', context)

class AddBudget(CreateView):
    template_name = 'finance/budget/add.html'
    model = Budget
    fields = '__all__'

    @method_decorator(permission_required('finance.add_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddBudget, self).dispatch(*args, **kwargs)

class ChangeBudget(UpdateView):
    template_name = 'finance/budget/change.html'
    model = Budget
    fields = '__all__'

    @method_decorator(permission_required('finance.change_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangeBudget, self).dispatch(*args, **kwargs)

class DeleteBudget(DeleteView):
    template_name = 'finance/budget/delete.html'
    model = Budget
    fields = '__all__'

    @method_decorator(permission_required('finance.delete_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteBudget, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.year = self.object.year
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('finance_budget', kwargs={'year': self.year})

class DuplicateBudget(FormView):
    template_name = 'finance/budget/duplicate.html'
    form_class = DuplicateBudgetForm

    def form_valid(self, form):
        print(form.cleaned_data)
        budgets = Budget.objects.filter(
            year = form.cleaned_data['fromYear']
        ).order_by('-type', 'category')

        self.toYear = form.cleaned_data['toYear']

        for budget in budgets:
            newBudget = Budget.objects.create(
                            year = self.toYear,
                            type = budget.type,
                            category = budget.category,
                            subCategory = budget.subCategory,
                            amount = budget.amount
                        )
        return super(DuplicateBudget, self).form_valid(form)

    def get_success_url(self):
        return reverse('finance_budget', kwargs={'year': self.toYear})

def transactionIndex(request):
    transactions = Transaction.objects.order_by('date')

    years = []
    for transaction in transactions:
        if transaction.date.year in years:
            continue
        years.append(transaction.date.year)

    context = {
        'years': years
    }
    return render(request, 'finance/transaction/index.html', context)

def transactionYear(request, year):
    previous_total = Transaction.objects.filter(
        date__lt = datetime(int(year), 1, 1)
    ).aggregate(total=Sum('amount', field="type*amount"))['total']

    transactions = Transaction.objects.filter(
        date__year = int(year)
    ).order_by('date', 'documentSerial', 'id')

    transactionList = []
    for transaction in transactions:
        transactionList.append({
            'id': transaction.id,
            'date': str(transaction.date.year) + '/' +
                    str(transaction.date.month) + '/' +
                    str(transaction.date.day),
            'serial': transaction.documentSerial,
            'category': transaction.category.name,
            'subCategory': transaction.subCategory.name if transaction.subCategory != None else '',
            'amount': transaction.type * transaction.amount,
            'payee': transaction.payee.name if request.user.is_authenticated() and transaction.payee != None else '',
            'comment': transaction.comment if request.user.is_authenticated() and transaction.comment != None else '',
        })

    context = {
        'year': year,
        'previous_total': previous_total if previous_total else 0,
        'transactionList': transactionList,
    }

    return render(request, 'finance/transaction/table.html', context)

def transactionYearMonth(request, year, month):
    previous_total = Transaction.objects.filter(
        date__lt = datetime(int(year), int(month), 1)
    ).aggregate(total=Sum('amount', field="type*amount"))['total']

    transactions = Transaction.objects.filter(
        date__year = int(year),
        date__month = int(month)
    ).order_by('date', 'documentSerial', 'id')

    transactionList = []
    for transaction in transactions:
        transactionList.append({
            'id': transaction.id,
            'date': str(transaction.date.year) + '/' +
                    str(transaction.date.month) + '/' +
                    str(transaction.date.day),
            'serial': transaction.documentSerial,
            'payee': transaction.payee.name if request.user.is_authenticated() and transaction.payee != None else '',
            'category': transaction.category.name,
            'subCategory': transaction.subCategory.name if transaction.subCategory != None else '',
            'amount': transaction.type * transaction.amount,
            'comment': transaction.comment if request.user.is_authenticated() and transaction.comment != None else '',
        })

    context = {
        'year': year,
        'month': month,
        'previous_total': previous_total if previous_total else 0,
        'transactionList': transactionList,
    }

    return render(request, 'finance/transaction/table.html', context)
    return render(request, 'finance/transaction/table.html', context)

class AddTransaction(CreateView):
    template_name = 'finance/transaction/add.html'
    model = Transaction
    fields = '__all__'

    @method_decorator(permission_required('finance.add_transaction', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddTransaction, self).dispatch(*args, **kwargs)

class ChangeTransaction(UpdateView):
    template_name = 'finance/transaction/change.html'
    model = Transaction
    fields = '__all__'

    @method_decorator(permission_required('finance.change_transaction', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangeTransaction, self).dispatch(*args, **kwargs)

class DeleteTransaction(DeleteView):
    template_name = 'finance/transaction/delete.html'
    model = Transaction
    fields = '__all__'

    @method_decorator(permission_required('finance.delete_transaction', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteTransaction, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.year = self.object.date.year
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('finance_transaction_year', kwargs={'year': self.year})
