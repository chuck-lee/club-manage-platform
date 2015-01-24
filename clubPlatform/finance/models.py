from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django import forms

# Create your models here.
class Payee(models.Model):
    name = models.CharField(max_length=200, verbose_name='名稱')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='名稱')
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name='科')
    name = models.CharField(max_length=200, verbose_name='名稱')
    def __str__(self):
        return self.category.name + " - " + self.name

TYPE = (
    (-1, '支出'),
    (1, '收入')
)

class Budget(models.Model):
    year = models.IntegerField(verbose_name='年度')
    type = models.IntegerField(choices=TYPE, default=-1, verbose_name='收支')
    category = models.ForeignKey(Category, verbose_name='科')
    subCategory = models.ForeignKey(SubCategory, blank=True, null=True, verbose_name='目')
    amount = models.IntegerField(verbose_name='金額')
    def __str__(self):
        result = "(" + str(self.year) + ") " + self.category.name
        if self.subCategory != None:
            result = result + " - " + self.subCategory.name
        result = result + " : " + str(self.amount)
        return result
    def get_absolute_url(self):
        return reverse('finance_budget', kwargs={'year': self.year})

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'

class Transaction(models.Model):
    date = models.DateField(verbose_name='日期')
    documentSerial = models.CharField(max_length=200, blank=True, null=True, verbose_name='票據編號')
    budget = models.ForeignKey(Budget, verbose_name='預算')
    amount = models.IntegerField(verbose_name='金額')
    payee = models.ForeignKey(Payee, blank=True, null=True, verbose_name='對象')
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name='附註')
    def __str__(self):
        result = "(" + str(self.date) + ") " + self.budget.category.name
        if self.budget.subCategory != None:
            result = result + " - " + self.budget.subCategory.name
        result = result + " : " + str(self.amount)
        return result
    def get_absolute_url(self):
        return reverse('finance_transaction_year',
                       kwargs={'year': self.date.year})

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
