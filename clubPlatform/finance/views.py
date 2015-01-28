from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from datetime import datetime
from finance.models import *
from finance.forms import *

################################
####### shared functions #######
################################
def _get_budget_years():
    budgets = Budget.objects.order_by('-year')

    years = []
    for budget in budgets:
        if budget.year in years:
            continue
        years.append(budget.year)

    return years

################################
######## View functions ########
################################

def index(request):
    context = {
        'years': _get_budget_years()
    }
    return render(request, 'finance/index.html', context)

@permission_required('finance.can_add_payee', raise_exception=True)
def payee(request):
    context = {
        'payees': Payee.objects.order_by('id')
    }
    return render(request, 'finance/payee/index.html', context)

@permission_required('finance.can_add_category', raise_exception=True)
def category(request):
    context = {
        'categories': Category.objects.order_by('id'),
        'subcategories': SubCategory.objects.order_by('category')
    }
    return render(request, 'finance/category/index.html', context)

def budgetIndex(request):
    context = {
        'years': _get_budget_years()
    }
    return render(request, 'finance/budget/index.html', context)

def budget(request, year):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type', 'category')
    budgetList = []
    for budget in budgets:
        try:
            budget_last_year = Budget.objects.get(
                year = int(year) - 1,
                type = budget.type,
                category = budget.category,
                subCategory = budget.subCategory
            )

            transaction_last_year = Transaction.objects.filter(
                date__year = int(year) - 1,
                budget = budget_last_year,
            ).aggregate(amount=Sum('amount'))['amount']

            budget_last_year = budget_last_year.amount
        except ObjectDoesNotExist:
            budget_last_year = 0
            transaction_last_year = 0

        budgetList.append({
            'id': budget.id,
            'type': '歲入' if budget.type == 1 else '歲出',
            'category': budget.category.name,
            'subCategory': budget.subCategory.name if budget.subCategory != None else '',
            'amount': budget.amount,
            'last_transaction': transaction_last_year if transaction_last_year != None else 0,
            'last_budget': budget_last_year if budget_last_year != None else 0,
        })

    context = {
        'year': year,
        'budgetList': budgetList,
    }
    return render(request, 'finance/budget/table.html', context)

def transactionIndex(request):
    # There must be a budget then transaction can be submmited.
    # So the year list of transaction equals year list of budget, and its faster.
    context = {
        'years': _get_budget_years()
    }
    return render(request, 'finance/transaction/index.html', context)

def transactionYear(request, year):
    previous_income = Transaction.objects.filter(
            date__lt = datetime(int(year), 1, 1),
            budget__type = 1
        ).aggregate(total=Sum('amount'))['total']
    previous_income = int(previous_income) if previous_income != None else 0

    previous_expense = Transaction.objects.filter(
            date__lt = datetime(int(year), 1, 1),
            budget__type = -1
        ).aggregate(total=Sum('amount'))['total']
    previous_expense = int(previous_expense) if previous_expense != None else 0

    previous_total = previous_income - previous_expense

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
            'category': transaction.budget.category.name,
            'subCategory': transaction.budget.subCategory.name if transaction.budget.subCategory != None else '',
            'amount': transaction.budget.type * transaction.amount,
            'payee': transaction.payee.name if request.user.is_authenticated() and transaction.payee != None else '',
            'comment': transaction.comment if request.user.is_authenticated() and transaction.comment != None else '',
        })

    context = {
        'year': year,
        'previous_total': previous_total,
        'transactionList': transactionList,
    }

    return render(request, 'finance/transaction/table.html', context)

def transactionYearMonth(request, year, month):
    previous_income = Transaction.objects.filter(
            date__lt = datetime(int(year), int(month), 1),
            budget__type = 1
        ).aggregate(total=Sum('amount'))['total']
    previous_income = int(previous_income) if previous_income != None else 0

    previous_expense = Transaction.objects.filter(
            date__lt = datetime(int(year), int(month), 1),
            budget__type = -1
        ).aggregate(total=Sum('amount'))['total']
    previous_expense = int(previous_expense) if previous_expense != None else 0

    previous_total = previous_income - previous_expense

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
            'category': transaction.budget.category.name,
            'subCategory': transaction.budget.subCategory.name if transaction.budget.subCategory != None else '',
            'amount': transaction.budget.type * transaction.amount,
            'payee': transaction.payee.name if request.user.is_authenticated() and transaction.payee != None else '',
            'comment': transaction.comment if request.user.is_authenticated() and transaction.comment != None else '',
        })

    context = {
        'year': year,
        'month': month,
        'previous_total': previous_total,
        'transactionList': transactionList,
    }

    return render(request, 'finance/transaction/table.html', context)

def reportIndex(request):
    context = {
        'years': _get_budget_years()
    }
    return render(request, 'finance/report/index.html', context)

def reportYear(request, year):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type', 'category')
    reportList = []
    for budget in budgets:
        transaction_amount = Transaction.objects.filter(
            date__year = int(year),
            budget = budget,
        ).aggregate(amount=Sum('amount'))['amount']

        reportList.append({
            'type': '歲入' if budget.type == 1 else '歲出',
            'category': budget.category.name,
            'subCategory': budget.subCategory.name if budget.subCategory != None else '',
            'budget_amount': budget.amount,
            'transaction_amount': transaction_amount if transaction_amount != None else 0,
        })

    context = {
        'year': year,
        'reportList': reportList,
    }
    return render(request, 'finance/report/table.html', context)

def reportYearMonth(request, year, month):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type', 'category')
    reportList = []
    for budget in budgets:
        transaction_amount_this_month = Transaction.objects.filter(
            date__year = int(year),
            date__month = int(month),
            budget = budget,
        ).aggregate(amount=Sum('amount'))['amount']

        transaction_amount_prev_months = Transaction.objects.filter(
            date__gte = datetime(int(year), 1, 1),
            date__lt = datetime(int(year), int(month), 1),
            budget = budget,
        ).aggregate(amount=Sum('amount'))['amount']

        reportList.append({
            'type': '歲入' if budget.type == 1 else '歲出',
            'category': budget.category.name,
            'subCategory': budget.subCategory.name if budget.subCategory != None else '',
            'budget_amount': budget.amount,
            'transaction_amount_this_month': transaction_amount_this_month if transaction_amount_this_month != None else 0,
            'transaction_amount_prev_months': transaction_amount_prev_months if transaction_amount_prev_months != None else 0,
        })

    context = {
        'year': year,
        'month': month,
        'reportList': reportList,
    }
    return render(request, 'finance/report/table.html', context)

################################
########  Form classes  ########
################################
class AddPayee(CreateView):
    template_name = 'finance/payee/add.html'
    model = Payee
    form_class = PayeeForm

    @method_decorator(permission_required('finance.add_payee', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddPayee, self).dispatch(*args, **kwargs)

class ChangePayee(UpdateView):
    template_name = 'finance/payee/change.html'
    model = Payee
    form_class = PayeeForm

    @method_decorator(permission_required('finance.change_payee', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangePayee, self).dispatch(*args, **kwargs)

class DeletePayee(DeleteView):
    template_name = 'finance/payee/delete.html'
    model = Payee
    fields = '__all__'

    @method_decorator(permission_required('finance.delete_payee', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeletePayee, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('finance_payee')


class AddCategory(CreateView):
    template_name = 'finance/category/addCategory.html'
    model = Category
    form_class = CategoryForm

    @method_decorator(permission_required('finance.add_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddCategory, self).dispatch(*args, **kwargs)

class ChangeCategory(UpdateView):
    template_name = 'finance/category/changeCategory.html'
    model = Category
    form_class = CategoryForm

    @method_decorator(permission_required('finance.change_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangeCategory, self).dispatch(*args, **kwargs)

class DeleteCategory(DeleteView):
    template_name = 'finance/category/deleteCategory.html'
    model = Category
    fields = '__all__'

    @method_decorator(permission_required('finance.delete_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteCategory, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('finance_category')

    def get_context_data(self, **kwargs):
        context = super(DeleteCategory, self).get_context_data(**kwargs)
        category = self.get_object()
        context['subcategories'] = SubCategory.objects.filter(category=category).count()
        context['budgets'] = Budget.objects.filter(subCategory__category=category).count()
        context['transactions'] = Transaction.objects.filter(budget__subCategory__category=category).count()
        return context


class AddSubCategory(CreateView):
    template_name = 'finance/category/addSubCategory.html'
    model = SubCategory
    form_class = SubCategoryForm

    @method_decorator(permission_required('finance.add_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddSubCategory, self).dispatch(*args, **kwargs)

class ChangeSubCategory(UpdateView):
    template_name = 'finance/category/changeSubCategory.html'
    model = SubCategory
    form_class = SubCategoryForm

    @method_decorator(permission_required('finance.change_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangeSubCategory, self).dispatch(*args, **kwargs)

class DeleteSubCategory(DeleteView):
    template_name = 'finance/category/deleteSubCategory.html'
    model = SubCategory
    fields = '__all__'

    @method_decorator(permission_required('finance.delete_category', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteSubCategory, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('finance_category')

    def get_context_data(self, **kwargs):
        context = super(DeleteSubCategory, self).get_context_data(**kwargs)
        subCategory = self.get_object()
        context['budgets'] = Budget.objects.filter(subCategory=subCategory).count()
        context['transactions'] = Transaction.objects.filter(budget__subCategory=subCategory).count()
        return context


class AddBudget(CreateView):
    template_name = 'finance/budget/add.html'
    model = Budget
    form_class = BudgetForm

    @method_decorator(permission_required('finance.add_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddBudget, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        return super(AddBudget, self).form_valid(form)

class ChangeBudget(UpdateView):
    template_name = 'finance/budget/change.html'
    model = Budget
    form_class = BudgetForm

    @method_decorator(permission_required('finance.change_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(ChangeBudget, self).dispatch(*args, **kwargs)

class DeleteBudget(DeleteView):
    template_name = 'finance/budget/delete.html'
    model = Budget
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(DeleteBudget, self).get_context_data(**kwargs)
        budget = self.get_object()
        transactions = Transaction.objects.filter(budget=budget).count()
        context['transactions'] = transactions
        return context

    @method_decorator(permission_required('finance.delete_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DeleteBudget, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        budget = self.get_object()
        self.year = budget.year
        budget.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('finance_budget', kwargs={'year': self.year})

class DuplicateBudget(FormView):
    template_name = 'finance/budget/duplicate.html'
    form_class = DuplicateBudgetForm

    @method_decorator(permission_required('finance.add_budget', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(DuplicateBudget, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
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

class AddTransaction(CreateView):
    template_name = 'finance/transaction/add.html'
    model = Transaction
    form_class = TransactionForm

    @method_decorator(permission_required('finance.add_transaction', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(AddTransaction, self).dispatch(*args, **kwargs)

class ChangeTransaction(UpdateView):
    template_name = 'finance/transaction/change.html'
    model = Transaction
    form_class = TransactionForm

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
