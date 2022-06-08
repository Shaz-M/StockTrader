from urllib import response
from wsgiref.util import request_uri
from xml.sax.handler import property_dom_node
from django.shortcuts import render
from portfolio.models import Portfolio
from .models import Stock
from .forms import OrderForm
from django.shortcuts import redirect
from .utils import getPrice, stockInfo,validateTicker,validateBuy,validateSell,getCompanyName

# Create your views here.

def ticker(request,tid):
    tid = tid.upper()
    if not validateTicker(tid):
        return redirect('dashboard')
    if(request.method == 'POST'):
        form = OrderForm(request.POST)
        if(form.is_valid):
            user = request.user
            orderType = request.POST['orderType']
            quantity = int(request.POST['quantity'])
            price = getPrice(tid);
            portfolio = Portfolio.objects.get(user=user)
            stockExits = portfolio.stock_set.filter(ticker=tid).exists()
            # check if user can afford the buy or has enough shares to sell
            # if the ticker alredy is in portfolio then we update the current postion otherwise make a new ticker model
            if(orderType == 'Buy'):
                if not validateBuy(price,quantity,portfolio):
                    #send a error message for not enough money
                    return redirect('ticker',tid=tid)
                elif(stockExits):
                    stockObj = portfolio.stock_set.get(ticker=tid)
                    cost = price*quantity
                    stockObj.avgPrice = (stockObj.avgPrice*stockObj.numShares + cost)/(stockObj.numShares+quantity)
                    stockObj.numShares+=quantity
                    portfolio.cashBalance -= cost
                    stockObj.save()
                else:
                    newModel = Stock(ticker=tid,avgPrice=price,numShares=quantity,portfolio=portfolio)
                    portfolio.cashBalance -= price*quantity
                    newModel.save()
                portfolio.save()
            else: #sell order
                if not stockExits or not validateSell(tid,price,quantity,portfolio):
                    return redirect('ticker',tid=tid)
                stockObj = portfolio.stock_set.get(ticker=tid)
                stockObj.numShares -=quantity
                portfolio.cashBalance+= quantity*price
                if(stockObj.numShares == 0):
                    stockObj.delete()
                else:
                    stockObj.save()
                portfolio.save()

    form = OrderForm()
    stockObj = stockInfo()
    stockObj.ticker = tid
    stockObj.fullName = getCompanyName(tid)
    context = {'stockObj':stockObj,'OrderForm':form}
    return render(request,'stocks/ticker.html',context)

