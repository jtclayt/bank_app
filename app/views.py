from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Account, AccountType, Transaction, TransactionType


def index(request):
    return redirect(reverse('app:accounts'))


@login_required()
def account_detail(request, account_id):
    context = {
        'user': request.user,
        # 'account': get_object_or_404(Account, id=account_id)
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
        print(request.POST)
        return redirect(reverse('app:accounts'))


class PurchaseView(LoginRequiredMixin, Main, View):
    template = 'purchase.html'

    def post(self, request):
        print(request.POST)
        return redirect(reverse('app:purchase'))


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
        print(request.POST)
        return redirect(reverse('app:contacts'))


class ExternalTransferView(LoginRequiredMixin, Main, View):
    template = 'ext_transfer.html'

    def get(self, request, contact_id):
        context = {
            'user': request.user,
            'accounts': request.user.accounts.all(),
            'contact': get_object_or_404(get_user_model(), id=contact_id)
        }
        return render(request, self.get_template, context)

    def post(self, request, contact_id):
        print(request.POST)
        return redirect(reverse('app:external_transfer', args=(contact_id,)))


class ATMView(LoginRequiredMixin, Main, View):
    template = 'atm.html'

    def post(self, request):
        print(request.POST)
        return redirect(reverse('app:atm'))

def edit_profile(request):
    return render(request, 'edit_profile.html')
