from termios import TIOCPKT_FLUSHREAD
from webbrowser import get
from django.shortcuts import redirect, render
from .forms import TickerForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Portfolio, accountBal, transactionHist
from stocks.utils import validateTicker
from django.contrib.auth.decorators import login_required
from .utils import topGainers,topLosers,getNews,getDoChartData,getAccountBal
from decimal import Decimal
from django.contrib import messages
import json

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    portfolio = Portfolio.objects.get(user=user)
    balanceHistory = portfolio.accountbal_set.exists()
    labels = []
    data = []
    #add all balances is the user has balance history
    if balanceHistory:
        balances = portfolio.accountbal_set.all()
        for balance in balances:
            labels.append(str(balance.date))
            data.append(str(balance.balance))
    gainers = topGainers()
    losers = topLosers()
    news = getNews()
    doChartLabels,doChartData,totalValue,totalReturn,dailyPL = getDoChartData(user)
    context = {
    'title':'Dashboard',
    'labels':json.dumps(labels),
    'data':json.dumps(data),
    'gainers':gainers,
    'losers':losers,
    'news':news,
    'doChartLabels':doChartLabels,
    'doChartData':doChartData,
    'totalValue':totalValue,
    'totalReturn':totalReturn,
    'dailyReturn':dailyPL,
    }
    return render(request,'portfolio/dashboard.html',context)

@login_required
def positions(request):
    user = request.user   
    portfolio = Portfolio.objects.get(user=user)
    stocks = portfolio.stock_set.all()
    cash = portfolio.cashBalance
    context = {'stocks':stocks, 'cash':cash}
    return render(request,'portfolio/positions.html',context)

@login_required
def account(request):
    user = request.user
    portfolio = Portfolio.objects.get(user=user)
    if(request.method == 'POST'):
        orderType = request.POST['orderType']
        bank = request.POST['radioname']
        amount = 0
        if(orderType == 'deposit'):
            amount = Decimal(request.POST['deposit'])
            portfolio.initialBalance+=amount
            portfolio.cashBalance+=amount
        else:
            amount = Decimal(request.POST['withdraw'])
            portfolio.initialBalance-=amount
            portfolio.cashBalance-=amount
            if(portfolio.cashBalance<0):
                messages.warning(request,f'Withdrawl amount greater than cash balance')
                return redirect('portfolio:account')
            amount = amount*-1
        newModel = transactionHist(bank=bank,change=amount,portfolio=portfolio)
        newModel.save()
        portfolio.save()
        return redirect('portfolio:account')
    cash = str(portfolio.cashBalance)
    balance = getAccountBal(user)
    accountBal = str(balance)
    remaining = str(balance-portfolio.cashBalance)
    doChartLabels = ['cash','r']
    doChartData = [cash,remaining]
    transactions = portfolio.transactionhist_set.all()
    context = {
        'cash':cash,
        'accountBal':accountBal,
        'doChartLabels':doChartLabels,
        'doChartData':doChartData,
        'transactions':transactions
        }
    return render(request,'portfolio/account.html',context)

def navsearch(request):
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            if not validateTicker(q):
                return HttpResponseRedirect('/dashboard')
            else:
                return redirect('stocks/'+q)
                
        else:
            return HttpResponseRedirect('/dashboard')