from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BankAccountForm, UserEditForm


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'user_edit_form': form})


@login_required
def bank_account_create_view(request):
    if request.method == 'POST':
        bank_account_form = BankAccountForm(request.POST)
        if bank_account_form.is_valid():
            bank_account_form.save()
            return redirect('account_create_success')
    else:
        form = BankAccountForm()
    return render(request, 'amyx_bank/account_create.html', {'bank_account_create_form': form})


@login_required
def card_create_view(request):
    return render(request, 'details/card_detail.html')


@login_required
def account_create_view(request):
    return render(request, 'details/account_detail.html')


def account_create_success(request):
    return render(request, 'amyx_bank/account_create_done.html')


@login_required
def edit_card(request):
    pass


@login_required
def edit_account(request):
    pass


def main(request):
    return render(request, 'amyx_bank/main.html')
