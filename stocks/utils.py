from contextlib import nullcontext
import requests
from decimal import Decimal
from numerize import numerize
from portfolio.models import Portfolio
import math

millnames = ['',' T',' M',' B',' Trillion']

def getPrepJson(ticker):
    url = "https://financialmodelingprep.com/api/v3/profile/"+ticker+"?apikey=fe82ca03e820e6d83d41d4aae63c55b9"
    response = requests.get(url)
    return response.json()

def getJson(ticker):
    url = 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B'
    response = requests.get(url)
    return response.json()

def getPrice(ticker):
    response = getJson(ticker)
    return Decimal(response[ticker].get('lastPrice'))


def validateTicker(ticker):
    response  = getJson(ticker)
    if not response:
        return False
    return True


def validateBuy(price,quantity,portfolio):
    totalCost = price*quantity
    if(portfolio.cashBalance < totalCost):
        return False
    return True

def validateSell(ticker,price,quantity,portfolio):
    stockObj = portfolio.stock_set.get(ticker=ticker)
    if(stockObj.numShares < quantity):
        return False
    return True

class stockInfo:
    ticker = None
    fullName = None
    prevClose = None
    volume = None
    description = None
    avgBuyPrice = None
    shares = None





def getStockObj(ticker,user):
    obj = stockInfo()
    response  = getJson(ticker)
    prepResponse = getPrepJson(ticker)
    portfolio = Portfolio.objects.get(user=user)
    stockExits = portfolio.stock_set.filter(ticker=ticker).exists()
    if stockExits:
        stockObj = portfolio.stock_set.get(ticker=ticker)
        obj.avgBuyPrice = stockObj.avgPrice
        obj.shares = stockObj.numShares
    obj.fullName = prepResponse[0].get('companyName')
    obj.ticker = ticker
    obj.volume = numerize.numerize(prepResponse[0].get('volAvg'))
    obj.prevClose = response[ticker].get('closePrice')
    obj.prevClose = math.floor(obj.prevClose*100)/100
    obj.description = prepResponse[0].get('description')
    return obj
