from django.shortcuts import redirect, render
from .forms import TickerForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Portfolio
from stocks.utils import validateTicker


# Create your views here.


def dashboard(request):   
    context = {'title':'Dashboard'}
    return render(request,'portfolio/dashboard.html',context)


def positions(request):
    user = request.user   
    portfolio = Portfolio.objects.get(user=user)
    stocks = portfolio.stock_set.all()
    context = {'stocks':stocks}
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