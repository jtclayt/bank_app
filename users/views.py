from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as logout_user
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from app.models import Account, AccountType


def index(request):
    return redirect(reverse('users:login'))


class Main(object):
    template = None

    def get(self, request):
        return render(request, self.get_template())

    def get_template(self):
        if self.template is not None:
            return self.template
        raise ImproperlyConfigured('Template not defined.')


class LoginView(Main, View):
    template = 'login.html'

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user)
            return redirect(reverse('app:index'))
        messages.error(request, 'Invalid credentials')
        return redirect(reverse('users:login'))


class RegisterView(Main, View):
    template = 'register.html'

    def post(self, request):
        errors = get_user_model().objects.validate_register(request.POST)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
            return redirect(reverse('users:register'))

        user = get_user_model().objects.create_user(
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            birthday=request.POST['dob']
        )
        Account.objects.create_account(
            owner=user,
            account_type=AccountType.objects.get(id=2)
        )
        login(request, user)
        return redirect('app:index')


class EditUserView(LoginRequiredMixin, Main, View):
    template = 'edit_profile.html'

    def post(self, request):
        errors = get_user_model().objects.validate_user_info(
            request.POST,
            request.user
        )
        print(errors)
        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
        else:
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.email = request.POST['email']
            request.user.save()
            messages.success(request, 'Account info updated!')
        return redirect(reverse('users:edit'))


@login_required()
def change_password(request):
    if request.method == 'POST':
        errors = {}
        if not request.user.check_password(request.POST['old_password']):
            errors['old_password'] = 'Password is incorrect'
        get_user_model().objects.validate_password(request.POST, errors)

        if len(errors) > 0:
            for key, error in errors.items():
                messages.error(request, error)
        else:
            request.user.set_password(request.POST['password'])
            request.user.save()
            login(request, request.user)
            messages.success(request, 'Password changed!')

    return redirect(reverse('users:edit'))


def logout(request):
    logout_user(request)
    return redirect(reverse('users:login'))
