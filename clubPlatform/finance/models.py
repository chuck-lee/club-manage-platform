from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django import forms

################################
###########  Models  ###########
################################
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
        result = "(" + str(self.year) + ") " + \
                ('支出 - ' if self.type == -1 else '收入 - ') + \
                self.category.name
        if self.subCategory != None:
            result = result + " - " + self.subCategory.name
        result = result + " : " + str(self.amount)
        return result
    def get_absolute_url(self):
        return reverse('finance_budget', kwargs={'year': self.year})
    def clean_fields(self, exclude = None):
        super(Budget, self).clean_fields(exclude)
        if self.subCategory != None and \
           self.subCategory.category != self.category:
            raise ValidationError({'subCategory': '科目不符'})

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
    def clean_fields(self, exclude = None):
        super(Transaction, self).clean_fields(exclude)
        if self.budget.year != self.date.year:
            raise ValidationError({'budget': '預算年度與收支紀錄年度不符'})

################################
#####  Model Form classes  #####
################################

class PayeeForm(forms.ModelForm):
    class Meta:
        model = Payee
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
