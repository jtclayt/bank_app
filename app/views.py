from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from users.models import Main


def index(request):
    return redirect(reverse('app:accounts'))


class AccountsView(LoginRequiredMixin, Main, View):
    login_url = '/users/login/'
    template = 'dashboard.html'

    def post(self, request):
        '''
        Route for posting a new account for a user.
        '''
        print(request.POST)
        return redirect(reverse('app:accounts'))


class AccountDetailView(Main, View):
    template = 'account_details.html'


def purchase(request):
    return render(request, 'purchase.html')

def transfer(request):
    return render(request, 'transfer.html')

def bill(request):
    return render(request, 'bill.html')

def extTransfer(request):
    return render(request, 'ext_transfer.html')

def extContacts(request):
    return render(request, 'transfer_contacts.html')

def atm(request):
    return render(request, 'atm.html')