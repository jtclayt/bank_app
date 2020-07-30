from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from .models import Account, AccountType, Transaction, TransactionType




def index(request):
    return redirect(reverse('app:accounts'))


@login_required()
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    context = {
        'user': request.user,
        'account': account,
        'interest_percent': account.account_type.interest_rate * 100,
        'transactions': account.transactions.all().order_by('-created_at')
    }
    return render(request,  'account_details.html', context)


class Main(object):
    template = None

    def get(self, request):
        context = {
            'user': request.user,
            'accounts': request.user.accounts.all()
        }
        return render(request, self.get_template(), context)

    def get_template(self):
        if self.template is not None:
            return self.template
        raise ImproperlyConfigured('Template not defined.')


class AccountsView(LoginRequiredMixin, Main, View):
    template = 'dashboard.html'

    def post(self, request):
        user = request.user
        created_account = Account.objects.create_account(
            owner=user,
            account_type=AccountType.objects.get(name=request.POST['account_name']),
            balance=0
        )

        account_type = created_account.account_type
        messages.success(request, 'You have successfully created a new '+account_type.name+' account! You can now transfer funds!')
        return redirect('/accounts/'+str(created_account.id))
        # return redirect(reverse('app:accounts'))


class PurchaseView(LoginRequiredMixin, Main, View):
    template = 'purchase.html'

    def post(self, request):
        errors = Transaction.objects.validate_purchase(request.POST)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
            return redirect(reverse('app:purchase'))

        selected_account = Account.objects.get(id=request.POST['account_id'])
        new_balance = selected_account.balance - int(request.POST['amount'])

        selected_account.balance = new_balance
        selected_account.save()

        Transaction.objects.create(
            desc = request.POST['desc'],
            amount = request.POST['amount'],
            new_balance = new_balance,
            is_deposit = False,
            process_date = request.POST['date'],
            account = selected_account,
            transaction_type = TransactionType.objects.get(name="Purchase")
        )

        messages.success(request, "You have successfully added a new purchase!")
        return redirect('/accounts/'+str(selected_account.id))


class TransferView(LoginRequiredMixin, Main, View):
    template = 'transfer.html'

    def post(self, request):
        print(request.POST)
        return redirect(reverse('app:transfer'))


class BillView(LoginRequiredMixin, Main, View):
    template = 'bill.html'

    def post(self, request):
        print(request.POST)
        return redirect(reverse('app:bill'))


class ContactsView(LoginRequiredMixin, Main, View):
    template = 'transfer_contacts.html'

    def post(self, request):
        errors = Account.objects.validate_contact(
            request.POST,
            request.user.id
        )
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
        else:
            account = get_object_or_404(
                Account,
                account_number=request.POST['account_number']
            )
            request.user.linked_accounts.add(account)
        return redirect(reverse('app:contacts'))


class ExternalTransferView(LoginRequiredMixin, Main, View):
    template = 'ext_transfer.html'

    def get(self, request, account_id):
        context = {
            'user': request.user,
            'accounts': request.user.accounts.all(),
            'contact': get_object_or_404(Account, id=account_id),
            'today': datetime.now().strftime('%Y-%m-%d')
        }
        return render(request, self.get_template(), context)

    def post(self, request, account_id):
        errors = Transaction.objects.validate_extransfer(request.POST)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
            return redirect(
                reverse('app:external_transfer', args=(account_id,))
            )

        to_acct = get_object_or_404(Account, id=account_id)
        from_acct = get_object_or_404(Account, id=request.POST['account'])
        trans_amount = float(request.POST['amount'])
        Transaction.objects.create(
            desc=request.POST['desc'],
            amount=trans_amount,
            new_balance=from_acct.balance - trans_amount,
            is_deposit=False,
            process_date=request.POST['date'],
            account=from_acct,
            transaction_type=TransactionType.objects.get(id=1),
        )
        Transaction.objects.create(
            desc=request.POST['desc'],
            amount=trans_amount,
            new_balance=to_acct.balance + trans_amount,
            is_deposit=True,
            process_date=request.POST['date'],
            account=to_acct,
            transaction_type=TransactionType.objects.get(id=1),
        )
        from_acct.balance -= trans_amount
        to_acct.balance += trans_amount
        from_acct.save()
        to_acct.save()
        messages.success(request, 'External transfer successfully processed')
        return redirect(reverse('app:accounts_detail', args=(from_acct.id,)))


class ATMView(LoginRequiredMixin, Main, View):
    template = 'atm.html'

    def post(self, request):
        errors = Transaction.objects.validate_atm(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(reverse('app:atm'))
        else:
            accounts = request.user.accounts.all()
            for account in accounts:
                if account.account_type.name == request.POST['account']:
                    this_account = account
            desc = request.POST['description']
            amount = request.POST['amount']
            if request.POST['type'] == "Withdrawal":
                new_balance = this_account.balance - float(request.POST['amount'])
                is_deposit = False
            elif request.POST['type'] == "Deposit":
                new_balance = this_account.balance + float(request.POST['amount'])
                is_deposit = True
            process_date = datetime.now()
            transaction_type = TransactionType.objects.get(name="ATM")
            transaction = Transaction.objects.create(
                desc = desc,
                amount = amount,
                new_balance = new_balance,
                is_deposit = is_deposit,
                process_date = process_date,
                account = this_account,
                transaction_type = transaction_type
            )
            this_account.balance = new_balance
            this_account.save()
            return redirect(reverse('app:accounts'))

@login_required()
def create_account(request):
    if request.method == 'GET':
        context = {
            'account_types': AccountType.objects.all()
        }
        return render(request, 'create_account.html', context)

