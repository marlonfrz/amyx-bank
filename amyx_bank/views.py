from django.contrib.auth import authenticate, login, logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from account.forms import UserRegistrationForm
from account.models import Profile

from .forms import AccountEditForm, AccountForm, CardCreateForm, CardEditForm, LoginForm
from .models import BankAccount, Card


def logout(request):
    return render(request, 'registration/logout.html')


def main(request):
    return render(request, 'amyx_bank/main.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def bank_account_create_view(request):
    if request.method == 'POST':
        bank_account_form = AccountForm(request.POST)
        if bank_account_form.is_valid():
            bank_account_form.save()
            return redirect('account_create_success')
    else:
        form = AccountForm()
    return render(request, 'account/account_create.html', {'bank_account_create_form': form})


def logout(request):
    log_out(request)
    return render(request, 'registration/logout.html')


@login_required
def main(request):
    return render(request, 'amyx_bank/main.html')


@login_required
def edit_bank_account(request, id):  # el pk es primarykey
    bank_account = BankAccount.objects.get(id=id)
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            return redirect('bank_account_detail', id=id)
    else:
        form = AccountEditForm(instance=bank_account)
    return render(request, 'edit_bank_account.html', {'account_edit_form': form})


@login_required
def card_create(request, id):  # el pk es primarykey
    if request.method == 'POST':
        form = CardCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('card_detail', id=id)
        else:
            form = CardCreateForm()
        return render(request, 'amyx_bank/card_create.html', {'card_create_form': form})


@login_required
def card_edit(request, id):  # el pk es primarykey
    card_id = Card.objects.get(id=id)
    if request.method == 'POST':
        form = CardEditForm(request.POST, instance=card_id)
        if form.is_valid():
            form.save()
            return redirect('card_detail', id=id)
    else:
        form = CardEditForm(instance=card_id)
    return render(request, 'card_edit.html', {'card_edit_form': form})
