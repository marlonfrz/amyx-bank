from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate

from account.models import BankAccount, Profile

from account.forms import ChangePasswordForm, AccountEditForm, AccountForm


# http://dsw.pc16.aula109:8000/account
@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    accounts = BankAccount.objects.filter(profile=profile)
    balance = sum(account.balance for account in accounts)
    return render(request, "account/dashboard.html", {"total_balance": balance})


# http://dsw.pc16.aula109:8000/account/account_create_success/
@login_required
def account_create_success(request):
    return render(request, "account/account_create_done.html")


# http://dsw.pc16.aula109:8000/account/edit/password
@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = ChangePasswordForm(request.user)
    return render(request, "account/change_password.html", {"change_password": form})


# http://dsw.pc16.aula109:8000/create_account
@login_required
def bank_account_create_view(request):
    MAX_ACCOUNT_AMOUNT = 4
    if request.method == "POST":
        bank_account_form = AccountForm(request.POST)
        if bank_account_form.is_valid():
            cd = bank_account_form.cleaned_data
            user = authenticate(
                request, username=request.user.username, password=cd["password"]
            )
            profile = get_object_or_404(Profile, user=request.user)
            accounts = BankAccount.objects.filter(profile=profile).exclude(status=BankAccount.Status.CANCELLED)
            if len(accounts) < MAX_ACCOUNT_AMOUNT:
                if user is not None:
                        new_bank_account = bank_account_form.save(commit=False)
                        profile = get_object_or_404(Profile, user=user)
                        new_bank_account.profile = profile
                        new_bank_account.save()
                        return redirect("dashboard")
                else:
                    return HttpResponse("Invalid credentials")
            else:
                return HttpResponseBadRequest("You have reached the max amount of accounts you can create, which is 4") 
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = AccountForm()
    return render(
        request, "account/account_create.html", {"bank_account_create_form": form}
    )


# http://dsw.pc16.aula109:8000/edit/account/<int:id>/
@login_required
def edit_bank_account(request, id):  # el pk es primarykey
    bank_account = BankAccount.objects.get(id=id)
    if request.method == "POST":
        form = AccountEditForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            return redirect("accounts")
    else:
        form = AccountEditForm(instance=bank_account)
    return render(request, "account/account_edit.html", {"account_edit_form": form})


# http://dsw.pc16.aula109:8000/account/accounts
@login_required
def accounts(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    accounts = BankAccount.objects.filter(profile=profile).exclude(status=BankAccount.Status.CANCELLED)
    return render(request, "account/accounts.html", {"accounts": accounts})


# http://dsw.pc16.aula109:8000/account/<id:int>
def account_detail(request, id):
    account = get_object_or_404(BankAccount, id=id)
    if account.status == BankAccount.Status.CANCELLED:
        return HttpResponseBadRequest("The account you tried to view was canceled some time ago")
    return render(request, "account/account_detail.html", {"account": account})