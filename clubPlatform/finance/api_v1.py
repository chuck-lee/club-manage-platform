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
        'user': request.user,
        'availableYears': Budget.objects.values('year').distinct().order_by('-year')
    }
    return render(request, 'finance/api/v1/availableYears.html', context)

def payees(request):
    if not (request.user.has_perm('finance.add_transaction') or request.user.has_perm('finance.change_transaction')) :
            raise PermissionDenied;

    context = {
        'payees': User.objects.all()
    }

    return render(request, 'finance/api/v1/payees.html', context)

def category(request):
    context = {
        'user': request.user,
        'categorys': Category.objects.all().order_by('id')
    }
    return render(request, 'finance/api/v1/category.html', context)

def subCategory(request):
    context = {
        'user': request.user,
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
            'subCategory': budget.subCategory,
            'amount': budget.amount,
            'last_transaction': transaction_last_year if transaction_last_year != None else 0,
            'last_budget': budget_last_year if budget_last_year != None else 0,
        })

    context = {
        'user': request.user,
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
        'user': request.user,
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
        'user': request.user,
        'year': year,
        'reports': reports,
    }
    return render(request, 'finance/api/v1/reportYear.html', context)

def budgetDetail(request, id):
    if request.method == "GET":
        # Get
        try:
            budget = Budget.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        context = {
            'user': request.user,
            'id': id,
            'budget': budget
        }

        return render(request, 'finance/api/v1/budgetDetail.html', context)
    elif request.method == "POST":
        # Create
        if not request.user.has_perm('finance.add_budget'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            subCategory = SubCategory.objects.get(pk = param['subCategoryId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

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

        param = json.loads(request.body.decode("utf-8"))

        try:
            budget = Budget.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        try:
            subCategory = SubCategory.objects.get(pk = param['subCategoryId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        budget.year = param['year']
        budget.type = param['type']
        budget.subCategory = subCategory
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

def categoryDetail(request, id):
    if request.method == "GET":
        # Get
        try:
            category = Category.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        context = {
            'user': request.user,
            'id': id,
            'category': category
        }

        return render(request, 'finance/api/v1/categoryDetail.html', context)
    elif request.method == "POST":
        # Create
        if not request.user.has_perm('finance.add_category'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            category = Category.objects.get(name = param['name'])
            raise SuspiciousOperation()
        except ObjectDoesNotExist:
            category = Category(name = param['name'])
            category.save()
            return HttpResponse()
    elif request.method == "PUT":
        # Update
        if not request.user.has_perm('finance.change_category'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            category = Category.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        category.name = param['name']
        category.save()
        return HttpResponse()
    elif request.method == "DELETE":
        # Delete
        if not request.user.has_perm('finance.delete_category'):
            raise PermissionDenied;

        try:
            category = Category.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        category.delete()

        return HttpResponse()

    return HttpResponseNotFound()

def subCategoryDetail(request, id):
    if request.method == "GET":
        # Get
        try:
            subCategory = SubCategory.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        context = {
            'user': request.user,
            'id': id,
            'subCategory': subCategory
        }

        return render(request, 'finance/api/v1/subCategoryDetail.html', context)
    elif request.method == "POST":
        # Create
        if not request.user.has_perm('finance.add_category'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            category = Category.objects.get(pk = param['categoryId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        try:
            subCategory = SubCategory.objects.get(category = category, name = param['name'])
            raise SuspiciousOperation()
        except ObjectDoesNotExist:
            subCategory = SubCategory(category = category, name = param['name'])
            subCategory.save()
            return HttpResponse()
    elif request.method == "PUT":
        # Update
        if not request.user.has_perm('finance.change_category'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            subCategory = SubCategory.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        try:
            category = Category.objects.get(pk = param['categoryId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        subCategory.name = param['name']
        subCategory.category = category
        subCategory.save()
        return HttpResponse()
    elif request.method == "DELETE":
        # Delete
        if not request.user.has_perm('finance.delete_budget'):
            raise PermissionDenied;

        try:
            subCategory = SubCategory.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        subCategory.delete()

        return HttpResponse()

    return HttpResponseNotFound()

def transactionDetail(request, id):
    if request.method == "GET":
        # Get
        try:
            transaction = Transaction.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        context = {
            'user': request.user,
            'id': id,
            'transaction': transaction
        }

        return render(request, 'finance/api/v1/transactionDetail.html', context)
    elif request.method == "POST":
        # Create
        if not request.user.has_perm('finance.add_transaction'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            budget = Budget.objects.get(pk = param['budgetId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        payee = None
        if 'payeeId' in param:
            try:
                payee = User.objects.get(pk = param['payeeId'])
            except ObjectDoesNotExist:
                payee = None

        transaction = Transaction(date = param['date'],
                                  documentSerial = param['serial'] if 'serial' in param else '',
                                  budget = budget,
                                  amount = param['amount'],
                                  payee = payee,
                                  submitBy = request.user,
                                  comment = param['comment'] if 'comment' in param else ''
                      )
        transaction.save()

        return HttpResponse()
    elif request.method == "PUT":
        # Update
        if not request.user.has_perm('finance.change_transaction'):
            raise PermissionDenied;

        param = json.loads(request.body.decode("utf-8"))

        try:
            transaction = Transaction.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        # Only submiter can change submiited item
        if transaction.submitBy != request.user:
            raise PermissionDenied;

        try:
            budget = Budget.objects.get(pk = param['budgetId'])
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        payee = None
        if 'payeeId' in param:
            try:
                payee = User.objects.get(pk = param['payeeId'])
            except ObjectDoesNotExist:
                payee = None

        transaction.date = param['date']
        if 'serial' in param:
            transaction.documentSerial = param['serial']
        transaction.budget = budget
        transaction.amount = param['amount']
        transaction.payee = payee
        if 'comment' in param:
            transaction.comment = param['comment']
        transaction.save()
        return HttpResponse()
    elif request.method == "DELETE":
        # Delete
        if not request.user.has_perm('finance.delete_transaction'):
            raise PermissionDenied;
            return;

        try:
            transaction = Transaction.objects.get(pk = id)
        except ObjectDoesNotExist:
            raise SuspiciousOperation()

        transaction.delete()

        return HttpResponse()

    return HttpResponseNotFound()