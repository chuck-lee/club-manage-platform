from django.conf.urls import patterns, url
from finance import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='finance_index'),
    url(r'^budget/?$', views.budgetIndex, name='finance_budget_index'),
    url(r'^budget/(?P<year>\d+)/?$', views.budget, name='finance_budget'),

    url(r'^budget/add/?$', views.AddBudget.as_view(), name='finance_budget_add'),
    url(r'^budget/change/(?P<pk>\d+)/?$', views.ChangeBudget.as_view(), name='finance_budget_change'),
    url(r'^budget/delete/(?P<pk>\d+)/?$', views.DeleteBudget.as_view(), name='finance_budget_delete'),
    url(r'^budget/duplicate/?$', views.DuplicateBudget.as_view(), name='finance_budget_duplicate'),

    url(r'^transaction/?$', views.transactionIndex, name='finance_transaction_index'),
    url(r'^transaction/(?P<year>\d+)/?$', views.transactionYear, name='finance_transaction_year'),
    url(r'^transaction/(?P<year>\d+)/(?P<month>\d+)/?$', views.transactionYearMonth, name='finance_transaction_year_month'),

    url(r'^transaction/add/?$', views.AddTransaction.as_view(), name='finance_transaction_add'),
    url(r'^transaction/change/(?P<pk>\d+)/?$', views.ChangeTransaction.as_view(), name='finance_transaction_change'),
    url(r'^transaction/delete/(?P<pk>\d+)/?$', views.DeleteTransaction.as_view(), name='finance_transaction_delete'),
)