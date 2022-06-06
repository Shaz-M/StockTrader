from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    currentBalance = models.DecimalField(max_digits=10, decimal_places=2)
    initialBalance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

