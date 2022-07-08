import requests
from decimal import Decimal
from numerize import numerize
from portfolio.models import Portfolio
import math

millnames = ['',' T',' M',' B',' Trillion']

def getPrepJson(ticker):
    url = "https://financialmodelingprep.com/api/v3/profile/"+ticker+"?apikey=5e861c0bf1235ee81d2cb64fe8d90012"
    response = requests.get(url)
    return response.json()

def getJson(ticker):
    url = 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B'
    response = requests.get(url)
    return response.json()

def getPrice(ticker):
    response = getJson(ticker)
    return round(Decimal(response[ticker].get('regularMarketLastPrice')),2)


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
    PEratio = None
    PEGratio = None
    PCFratio = None
    DEratio = None
    marketCap = None
    beta = None
    dividend = None
    eps = None





def getStockObj(ticker,user):
    obj = stockInfo()
    response  = getJson(ticker)
    prepResponse = getPrepJson(ticker)
    financials = requests.get('https://api.tdameritrade.com/v1/instruments?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B&symbol='+ticker+'&projection=fundamental')
    financials = financials.json()
    financials = financials[ticker].get('fundamental')
    marketCap = requests.get('https://financialmodelingprep.com/api/v3/market-capitalization/'+ticker+'?apikey=5e861c0bf1235ee81d2cb64fe8d90012')
    marketCap = marketCap.json()
    marketCap = marketCap[0].get('marketCap')    
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
    obj.PEratio = financials.get('peRatio')
    obj.PEGratio = financials.get('pegRatio')
    obj.PCFratio = financials.get('pcfRatio')
    obj.DEratio = financials.get('totalDebtToEquity')
    obj.marketCap = numerize.numerize(marketCap)
    obj.beta = financials.get('beta')
    obj.dividend = financials.get('dividendAmount')
    obj.eps = financials.get('epsTTM')
    return obj