from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime


# Validations
class TransactionManager(models.Manager):
    # Log a purchase
    def validate_purchase(self, postData):
        errors = {}
        todaysDate = datetime.now().date()
        if postData['date'] > todaysDate:
            errors['date'] = "Purchase must've been made today or in the past"

        if len(postData['desc']) < 2:
            errors['desc'] = "Description must be greater that 2 characters"

        if not postData['amount'] > 0:
            errors['amount'] = "Amount must be greater than 0"
        return errors

    # Make a transfer
    def validate_transfer(self, postData):
        errors = {}
        if not postData['amount'] > 0:
            errors['amount'] = "Amount must be greater than 0"
        return errors

    # Pay a Bill
    def validate_bill(self, postData):
        errors = {}
        if not postData['account_number'] > 0:
            errors['account_number'] = "Account number must be greater than 0"
        if not postData['amount'] > 0:
            errors['amount'] = "Amount must be greater than 0"
        todaysDate = datetime.now().date()
        if postData['date'] > todaysDate:
            errors['date'] = "Date must be today or a future date"
        if len(postData['note']) < 2:
            errors['note'] = "Note must be greater that 2 characters"
        return errors

    # External Transfer
    def validate_extransfer(self, postData):
        errors = {}
        if not postData['account_number'] > 0:
            errors['account_number'] = "Account number must be greater than 0"
        if not postData['amount'] > 0:
            errors['amount'] = "Amount must be greater than 0"
        todaysDate = datetime.now().date()
        if postData['date'] > todaysDate:
            errors['date'] = "Date must be today or a future date"
        if len(postData['note']) < 2:
            errors['note'] = "Note must be greater that 2 characters"
        return errors

    # ATM Transaction
    def validate_atm(self, postData):
        errors = {}
        if not postData['amount'] > 0:
            errors['amount'] = "Amount must be greater than 0"
        return errors


# Models
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountType(BaseModel):
    name = models.CharField(max_length=100)
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
    objects = TransactionManager()
