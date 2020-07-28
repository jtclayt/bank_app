from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountType(BaseModel):
    name = models.CharField(max_length=100)
    withdrawal_limit = models.SmallIntegerField()
    interest_rate = models.FloatField()


class Account(BaseModel):
    account_number = models.CharField(max_length=16)
    balance = models.FloatField()
    owner = models.ForeignKey(
        get_user_model(),
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_type = models.ForeignKey(
        AccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    linked_accounts = models.ManyToManyField(
        "self",
        related_name='linked_accounts'
    )


class TransactionType(BaseModel):
    name = models.CharField(max_length=100)
    fee_amount = models.FloatField()


class Transaction(BaseModel):
    desc = models.CharField(max_length=255)
    amount = models.FloatField()
    new_balance = models.FloatField()
    is_deposit = models.BooleanField()
    process_date = models.DateField()
    account = models.ForeignKey(
        Account,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        related_name='transactions',
        on_delete=models.CASCADE
    )
