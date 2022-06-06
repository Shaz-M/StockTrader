from django.db import models
from portfolio.models import Portfolio

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    numShares = models.IntegerField();
    avgPrice = models.DecimalField(max_digits=6, decimal_places=2)
    portfolio = models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    def __str__(self):
        return self.ticker