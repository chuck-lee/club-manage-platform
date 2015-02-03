from django.conf.urls import patterns, url
from finance import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='finance_index'),

    url(r'^category/?$', views.category, name='finance_category'),
    url(r'^category/add/?$', views.AddCategory.as_view(), name='finance_category_add'),
    url(r'^category/change/(?P<pk>\d+)/?$', views.ChangeCategory.as_view(), name='finance_category_change'),
    url(r'^category/delete/(?P<pk>\d+)/?$', views.DeleteCategory.as_view(), name='finance_category_delete'),
    url(r'^category/addSub/?$', views.AddSubCategory.as_view(), name='finance_subcategory_add'),
    url(r'^category/changeSub/(?P<pk>\d+)/?$', views.ChangeSubCategory.as_view(), name='finance_subcategory_change'),
    url(r'^category/deleteSub/(?P<pk>\d+)/?$', views.DeleteSubCategory.as_view(), name='finance_subcategory_delete'),

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

    url(r'^report/?$', views.reportIndex, name='finance_report_index'),
    url(r'^report/(?P<year>\d+)/?$', views.reportYear, name='finance_report_year'),
    url(r'^report/(?P<year>\d+)/(?P<month>\d+)/?$', views.reportYearMonth, name='finance_report_year_month'),
)