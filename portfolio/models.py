from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    initialBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cashBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# keep track of daily balance for charting
class accountBal(models.Model):
    date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    portfolio = models.ForeignKey(Portfolio,on_delete=models.CASCADE)

    def __str__(self):
        return self.portfolio.user.username