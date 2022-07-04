from django.shortcuts import redirect, render
from .forms import TickerForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Portfolio
from stocks.utils import validateTicker
from django.contrib.auth.decorators import login_required
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
            print(balance.date)
            labels.append(str(balance.date))
            data.append(str(balance.balance))
    context = {'title':'Dashboard','labels':json.dumps(labels),'data':json.dumps(data)}
    return render(request,'portfolio/dashboard.html',context)

@login_required
def positions(request):
    user = request.user   
    portfolio = Portfolio.objects.get(user=user)
    stocks = portfolio.stock_set.all()
    cash = portfolio.cashBalance
    context = {'stocks':stocks, 'cash':cash}
    return render(request,'portfolio/positions.html',context)

def navsearch(request):
        if 'q' in request.GET and request.GET['q']:
            q = request.GET['q']
            if not validateTicker(q):
                return HttpResponseRedirect('/dashboard')
            else:
                return redirect('stocks/'+q)
                
        else:
            return HttpResponseRedirect('/dashboard')