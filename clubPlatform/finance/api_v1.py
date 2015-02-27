from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, SuspiciousOperation
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
import json

from datetime import datetime
from finance.models import *
from finance.forms import *

################################
######## View functions ########
################################
def availableYears(request):
    context = {
        'availableYears': Budget.objects.values('year').distinct().order_by('-year')
    }
    return render(request, 'finance/api/v1/availableYears.html', context)

def subCategory(request):
    context = {
        'subCategorys': SubCategory.objects.all().order_by('id')
    }
    return render(request, 'finance/api/v1/subCategory.html', context)

def budgetYear(request, year):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type')

    budgetList = []
    for budget in budgets:
        try:
            budget_last_year = Budget.objects.get(
                year = int(year) - 1,
                type = budget.type,
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
            'type': '收入' if budget.type == 1 else '支出',
            'category': budget.subCategory.category.name,
            'subCategory': budget.subCategory.name,
            'amount': budget.amount,
            'last_transaction': transaction_last_year if transaction_last_year != None else 0,
            'last_budget': budget_last_year if budget_last_year != None else 0,
        })

    context = {
        'year': year,
        'budgets': budgetList
    }
    return render(request, 'finance/api/v1/budgetYear.html', context)

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

    context = {
        'year': year,
        'previousTotal': previous_total,
        'transactions': Transaction.objects.filter(
                            date__year = int(year)
                        ).order_by('date', 'documentSerial', 'budget')
    }
    return render(request, 'finance/api/v1/transactionYear.html', context)

def reportYear(request, year):
    budgets = Budget.objects.filter(
        year = int(year)
    ).order_by('-type')
    reports = []
    for budget in budgets:
        transaction_amount = Transaction.objects.filter(
            date__year = int(year),
            budget = budget,
        ).aggregate(amount=Sum('amount'))['amount']

        reports.append({
            'type': '收入' if budget.type == 1 else '支出',
            'category': budget.subCategory.category.name,
            'subCategory': budget.subCategory.name,
            'budget': budget.amount,
            'transaction': transaction_amount if transaction_amount != None else 0,
        })

    context = {
        'year': year,
        'reports': reports,
    }
    return render(request, 'finance/api/v1/reportYear.html', context)

def budgetDetail(request, id):
    if request.method == "GET":
        # Get
        budget = Budget.objects.get(
            pk = int(id)
        )

        context = {
            'id': id,
            'budget': budget
        }

        return render(request, 'finance/api/v1/budgetDetail.html', context)
    elif request.method == "POST":
        # Create
        if not request.user.has_perm('finance.add_budget'):
            raise PermissionDenied;
            return;
        param = json.loads(request.body.decode("utf-8"))
        subCategory = SubCategory.objects.get(pk = param['subCategoryId'])

        try:
            budget = Budget.objects.get(year = param['year'], type = param['type'], subCategory = subCategory)
            raise SuspiciousOperation()
        except ObjectDoesNotExist:
            budget = Budget(year = param['year'], type = param['type'], subCategory = subCategory, amount = param['amount'])
            budget.save()
            return HttpResponse()
    elif request.method == "PUT":
        # Update
        if not request.user.has_perm('finance.change_budget'):
            raise PermissionDenied;
            return;
        param = json.loads(request.body.decode("utf-8"))

        try:
            budget = Budget.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        budget.year = param['year']
        budget.type = param['type']
        budget.subCategory = SubCategory.objects.get(pk = param['subCategoryId'])
        budget.amount = param['amount']
        budget.save()
        return HttpResponse()
    elif request.method == "DELETE":
        # Delete
        if not request.user.has_perm('finance.delete_budget'):
            raise PermissionDenied;
            return;
        try:
            budget = Budget.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        budget.delete()

        return HttpResponse()

    return HttpResponseNotFound()