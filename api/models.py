from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)

    @classmethod
    def create_wallet_for_user(cls,user):
        return cls.objects.create(user=user)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    transaction_type = models.CharField(max_length=15, choices=[('deposit','Deposit'),('withdrawal','Withdrawal')])
    timestamp = models.DateTimeField(auto_now_add=True)