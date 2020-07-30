from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError


class AccountManager(models.Manager):
    def validate_account(self, postData):
        errors = {}
        if len(Account.objects.filter(id=postData['account_type'])) == 0:
            errors['account_type'] = 'Select a valid account type'
        if postData['balance'] < 0:
            errors['balance'] = 'Balance must be greater than 0'
        return errors

    def validate_contact(self, postData, user_id):
        errors = {}
        account = Account.objects.filter(
            account_number=postData['account_number']
        )
        if len(account) > 0:
            account = account[0]
            if account.owner.first_name != postData['first_name']:
                errors['first_name'] = 'First name does not match'
            if account.owner.last_name != postData['last_name']:
                errors['last_name'] = 'Last name does not match'
            if account.owner.id == user_id:
                errors['owner'] = 'You cannot link your own account'
            if account.account_type.name == 'Credit':
                errors['account_type'] = 'Can\'t link to a credit account'
        else:
            errors['account_number'] = 'Account number does not exist'
        return errors

    def create_account(self, owner, account_type, balance=5):
        if not owner:
            raise ValueError('Account must have an owner')
        if not account_type:
            raise ValueError('Account must have a type')

        account = self.create(
            balance=balance,
            owner=owner,
            account_type=account_type
        )
        account.account_number = str(self.get_account_number(account.id))
        account.save()
        return account

    def get_account_number(self, id):
        return 7840000 + id


class TransactionManager(models.Manager):
    # Log a purchase
    def validate_purchase(self, postData):
        errors = {}
        todaysDate = datetime.now().date()

        if len(postData['date']) == 0:
            errors['date'] = "Please enter a date"
        elif datetime.strptime(postData['date'], "%Y-%m-%d").date() > todaysDate:
            errors['date'] = "Purchase must've been made today or in the past"

        if len(postData['desc']) < 2:
            errors['desc'] = "Description must be greater that 2 characters"

        if len(postData['amount']) == 0:
            errors['amount'] = "Please enter an amount!"
        elif not int(postData['amount']) > 0:
            errors['amount'] = "Amount must be greater than $0"

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
        if not float(postData['amount']) > 0:
            errors['amount'] = "Amount must be greater than 0"
        try:
            account = Account.objects.filter(id=postData['account'])
            if len(account) > 0:
                account = account[0]
                if float(postData['amount']) > account.balance:
                    errors['balance'] = 'Insufficient funds for transfer'
            else:
                errors['account'] = 'Please transfer from a valid account'
        except MultiValueDictKeyError:
            errors['account'] = 'Please select an account to transfer from'
        todays_date = datetime.now().date()
        transfer_date = datetime.strptime(postData['date'], "%Y-%m-%d").date()
        if transfer_date < todays_date:
            errors['date'] = "Date must be today or a future date"
        if len(postData['desc']) < 2:
            errors['note'] = "Note must be greater that 2 characters"
        return errors

    # ATM Transaction
    def validate_atm(self, postData):
        errors = {}
        if  len(postData['amount']) <= 0:
            errors['amount'] = "Amount must be greater than $0.00"
        if postData['account'] == "-Choose an Account-":
            errors['account'] = "Please select an account."
        if len(postData['type']) <= 0:
            errors['type'] = "You must select Withdrawal or Deposit."
        if len(postData['description']) <= 0:
            errors['description'] = "Enter a short description for this transaction."
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

    def __str__(self):
        return self.name


class Account(BaseModel):
    account_number = models.CharField(max_length=8, default='')
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
    linked_users = models.ManyToManyField(
        get_user_model(),
        related_name='linked_accounts'
    )
    objects = AccountManager()


class TransactionType(BaseModel):
    name = models.CharField(max_length=100)
    fee_amount = models.FloatField()

    def __str__(self):
        return self.name


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

