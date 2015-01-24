from django.core.urlresolvers import reverse
from django.db import models
from django.forms import ModelForm

# Create your models here.
class Payee(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.category.name + " - " + self.name

TYPE = (
    (-1, '支出'),
    (1, '收入')
)

class Budget(models.Model):
    year = models.IntegerField()
    type = models.IntegerField(choices=TYPE, default=-1)
    category = models.ForeignKey(Category)
    subCategory = models.ForeignKey(SubCategory, blank=True, null=True)
    amount = models.IntegerField()
    def __str__(self):
        result = "(" + str(self.year) + ") " + self.category.name
        if self.subCategory != None:
            result = result + " - " + self.subCategory.name
        result = result + " : " + str(self.amount)
        return result
    def get_absolute_url(self):
        return reverse('finance_budget', kwargs={'year': self.year})

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'

class Transaction(models.Model):
    date = models.DateField()
    documentSerial = models.CharField(max_length=200, blank=True, null=True)
    type = models.IntegerField(choices=TYPE, default=-1)
    amount = models.IntegerField()
    payee = models.ForeignKey(Payee, blank=True, null=True)
    category = models.ForeignKey(Category)
    subCategory = models.ForeignKey(SubCategory, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        result = "(" + str(self.date.year) + ") " + self.category.name
        if self.subCategory != None:
            result = result + " - " + self.subCategory.name
        result = result + " : " + str(self.amount)
        return result
    def get_absolute_url(self):
        return reverse('finance_transaction_year',
                       kwargs={'year': self.date.year})

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
