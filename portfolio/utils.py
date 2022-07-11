from distutils import archive_util
from django.http import response
from .models import Portfolio
from decimal import Decimal
import requests

class stockMover:
    symbol = None
    price = None
    name = None
    change = None
    percent = None

class NewsObj:
    author = None
    source = None
    title = None
    url = None
    imageUrl = None
    dateTime = None


#take in ticker return a list of the top 5 stock movers 
def topGainers():
    url = 'https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=5e861c0bf1235ee81d2cb64fe8d90012'
    response = requests.get(url)
    response = response.json()
    gainers = []
    for i in range(5):
        obj = stockMover()
        obj.symbol = response[i].get('symbol')
        obj.name = response[i].get('name')
        obj.price = round(response[i].get('price'),2)
        obj.change = round(response[i].get('change'),2)
        obj.percent = round(response[i].get('changesPercentage'),2)
        gainers.append(obj)
    return gainers
        

def topLosers():
    url = 'https://financialmodelingprep.com/api/v3/stock_market/losers?apikey=5e861c0bf1235ee81d2cb64fe8d90012'
    response = requests.get(url)
    response = response.json()
    losers = []
    for i in range(5):
        obj = stockMover()
        obj.symbol = response[i].get('symbol')
        obj.name = response[i].get('name')
        obj.price = round(response[i].get('price'),2)
        obj.change = abs(round(response[i].get('change'),2))
        obj.percent = abs(round(response[i].get('changesPercentage'),2))
        losers.append(obj)
    return losers

def getNews():
    url = 'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=9f070c3650844cbba78e8c2024befa22&pageSize=4'
    response = requests.get(url)
    response = response.json()
    articles = response.get('articles')
    newsArr = []
    for i in range(4):
        obj = NewsObj()
        obj.source = articles[i].get('source').get('name')
        obj.author = articles[i].get('author')
        obj.url = articles[i].get('url')
        obj.imageUrl = articles[i].get('urlToImage')
        obj.title = articles[i].get('title').split('-',1)[0]
        obj.dateTime = articles[i].get('publishedAt')
        newsArr.append(obj)
    return newsArr

#return all stocks weight and 
def getDoChartData(user):
    data = []
    labels = []
    totalValue = 0
    dailyPL = 0
    portfolio = Portfolio.objects.get(user=user)
    stocks = portfolio.stock_set.all()
    for stock in stocks:
        labels.append(stock.ticker)
        price,change = getPriceChange(stock.ticker)
        totalValue+=price*stock.numShares
        dailyPL+=stock.numShares*change
        data.append(str(price*stock.numShares))
    labels.append('Cash')
    data.append(str(portfolio.cashBalance))
    totalValue+=portfolio.cashBalance
    totalReturn = totalValue-portfolio.initialBalance
    return labels,data,totalValue,totalReturn,dailyPL
        
    
def getPriceChange(ticker):
    url = 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/quotes?apikey=D57TGYGPEEXE5IQRTHZG4EVDBATABE3B'
    response = requests.get(url)
    response = response.json()
    price = round(Decimal(response[ticker].get('regularMarketLastPrice')),2)
    change = round(Decimal(response[ticker].get('netChange')),2)
    return price,change

def getNewsTicker(ticker):
    url = 'https://newsapi.org/v2/everything?q='+ticker+'&sortBy=publishedAt&apiKey=9f070c3650844cbba78e8c2024befa22&pageSize=4'
    response = requests.get(url)
    response = response.json()
    articles = response.get('articles')
    newsArr = []
    for i in range(4):
        obj = NewsObj()
        obj.source = articles[i].get('source').get('name')
        obj.author = articles[i].get('author')
        obj.url = articles[i].get('url')
        obj.imageUrl = articles[i].get('urlToImage')
        obj.title = articles[i].get('title').split('-',1)[0]
        obj.dateTime = articles[i].get('publishedAt')
        newsArr.append(obj)
    return newsArr