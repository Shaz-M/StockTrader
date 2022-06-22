from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Portfolio(models.Model):
    initialBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cashBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

