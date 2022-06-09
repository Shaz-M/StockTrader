from contextlib import nullcontext
import requests
from decimal import Decimal


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





def getStockObj(ticker):
    response  = getJson(ticker)
    obj = stockInfo()
    obj.fullName = response[ticker].get('description')
    obj.ticker = ticker
    obj.prevClose = response[ticker].get('closePrice')
    return obj
