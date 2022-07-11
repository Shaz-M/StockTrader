from urllib import response
from wsgiref.util import request_uri
from xml.sax.handler import property_dom_node
from django.shortcuts import render
from portfolio.models import Portfolio
from .models import Stock
from django.shortcuts import redirect
from .utils import getPrice,validateTicker,validateBuy,validateSell,getStockObj
from portfolio.utils import getNewsTicker
# Create your views here.

def ticker(request,tid):
    tid = tid.upper()
    user = request.user
    if not validateTicker(tid):
        return redirect('dashboard')
    if(request.method == 'POST'):
        orderType = request.POST['orderType']
        quantity = int(request.POST['quantity'])
        price = getPrice(tid)
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
    portfolio = Portfolio.objects.get(user=user)
    cash = portfolio.cashBalance
    stockObj = getStockObj(tid,user)
    newsObj = getNewsTicker(tid)
    context = {'stockObj':stockObj,'newsObj':newsObj,'ticker':tid,'cash':cash}
    return render(request,'stocks/ticker.html',context)

