from huey import crontab
from huey.contrib.djhuey import periodic_task
from django.contrib.auth import get_user_model
from .models import Portfolio,accountBal
from stocks.utils import getPrice

# execute at 5pm everyday to record balance
@periodic_task(crontab(minute=0,hour=22))
def saveDailyBal():
    User = get_user_model()
    users = User.objects.all()

    # for each user in the database find the end of day balance and save to the model
    for currUser in users:
        portfolio = Portfolio.objects.get(user=currUser)
        stocks = portfolio.stock_set.all()
        netLiq = portfolio.cashBalance
        for stock in stocks:
            netLiq+= getPrice(stock.ticker)*stock.numShares

        newModel = accountBal(balance=netLiq,portfolio=portfolio)
        newModel.save()
    print('Model saved to database')