from account.forms import AccountEditForm, AccountForm, ChangePasswordForm
from account.models import BankAccount, Profile
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render


# http://dsw.pc16.aula109:8000/account
@login_required
def dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    accounts = (
        BankAccount.objects.filter(profile=profile)
        .exclude(status=BankAccount.Status.CANCELLED)
        .exclude(status=BankAccount.Status.DISABLED)
    )
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
            user = authenticate(request, username=request.user.username, password=cd["password"])
            profile = get_object_or_404(Profile, user=request.user)
            accounts = BankAccount.objects.filter(profile=profile).exclude(
                status=BankAccount.Status.CANCELLED
            )
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
                return HttpResponseBadRequest(
                    "You have reached the max amount of accounts you can create, which is 4"
                )
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = AccountForm()
    return render(request, "account/account_create.html", {"bank_account_create_form": form})


# http://dsw.pc16.aula109:8000/edit/account/<int:id>/
@login_required
def edit_bank_account(request, id):
    account = BankAccount.objects.get(id=id)
    if request.method == "POST":
        form = AccountEditForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data
            account_status = cd["status"]
            if account_status == BankAccount.Status.CANCELLED:
                return render(
                    request, "account/cancellation.html", {"account_name": cd["account_name"]}
                )
            return redirect("accounts")
    else:
        form = AccountEditForm(instance=account)
    return render(request, "account/account_edit.html", {"account_edit_form": form})


# http://dsw.pc16.aula109:8000/account/accounts
@login_required
def accounts(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    accounts = profile.accounts.exclude(status=BankAccount.Status.CANCELLED)
    #    accounts = BankAccount.objects.filter(profile=profile).
    #    exclude(status=BankAccount.Status.CANCELLED)
    return render(request, "account/accounts.html", {"accounts": accounts})


# http://dsw.pc16.aula109:8000/account/<id:int>
def account_detail(request, id):
    account = get_object_or_404(BankAccount, id=id)
    if account.status == BankAccount.Status.CANCELLED:
        return HttpResponseBadRequest("The account you tried to view was canceled some time ago")
    return render(request, "account/account_detail.html", {"account": account})
