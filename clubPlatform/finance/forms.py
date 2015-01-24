from django import forms

class DuplicateBudgetForm(forms.Form):
    fromYear = forms.IntegerField(label='參考年度')
    toYear = forms.IntegerField(label='建立年度')
