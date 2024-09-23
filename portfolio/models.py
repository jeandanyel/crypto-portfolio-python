from django.db import models
from django.utils import timezone

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=200)
    ticker_symbol = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cryptocurrency.name

class Transaction(models.Model):
    class Type(models.TextChoices):
        BUY = 'buy', 'Buy'
        SELL = 'sell', 'Sell'
        SEND = 'send', 'Send'
        RECEIVE = 'receive', 'Receive'
        TRANSFER = 'transfer', 'Transfer'
        TRADE = 'trade', 'Trade'
        SWAP = 'swap', 'Swap'

    type = models.CharField(max_length=255, choices=Type.choices, default=Type.BUY)
    fee = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    transacted_quantity = models.FloatField(null=True, blank=True)
    received_quantity = models.FloatField(null=True, blank=True)

    transacted_asset = models.ForeignKey(
        'Asset', 
        on_delete=models.CASCADE, 
        related_name='transactions_as_transacted',
        null=True
    )

    received_asset = models.ForeignKey(
        'Asset', 
        on_delete=models.CASCADE, 
        related_name='transactions_as_received',
        null=True
    )

    def __str__(self):
        return f"{self.type} transaction on {self.date}"
