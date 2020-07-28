from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User


def index(request):
    return render(request, 'dashboard.html')

def accountDetails(request):
    return render(request, 'account_details.html')

def purchase(request):
    return render(request, 'purchase.html')

