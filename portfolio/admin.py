from django.contrib import admin
from .models import Portfolio,accountBal, transactionHist

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(accountBal)
admin.site.register(transactionHist)