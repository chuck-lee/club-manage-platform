from django.contrib import admin
from finance.models import *

# Register your models here.
admin.site.register(Payee)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Budget)
admin.site.register(Transaction)
