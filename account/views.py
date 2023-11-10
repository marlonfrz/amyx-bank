from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from amyx_bank.models import BankAccount
from .models import Profile

from .forms import ChangePasswordForm, ProfileEditForm, UserEditForm


# http://dsw.pc16.aula109:8000/account
@login_required
def dashboard(request):
    #    bank_accounts = BankAccount.objects.filter(user=request.user.profile)
    return render(request, "account/dashboard.html")


# http://dsw.pc16.aula109:8000/account/account_create_success/
@login_required
def account_create_success(request):
    return render(request, "account/account_create_done.html")


# http://dsw.pc16.aula109:8000/account/edit/profile
@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("dashboard")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit_profile.html",
        {"user_edit_form": user_form, "profile_edit_form": profile_form},
    )


# http://dsw.pc16.aula109:8000/account/edit/password
@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ChangePasswordForm(request.user)
    return render(request, "account/change_password.html", {"change_password": form})


# http://dsw.pc16.aula109:8000/account/accounts
@login_required
def accounts(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    accounts = BankAccount.objects.filter(profile=profile).exclude(status=BankAccount.Status.CANCELLED)
    return render(request, "account/accounts.html", {"accounts": accounts})


# def list_cards(request, account_id):
#      cards = Card.objects.all().filter(account=account_id)
#      return render(request, "account/list_cards.html", {"cards": cards})
#
#
#
#
#

""" 
def account_list(request):
    account_list = BankAccount.objects.filter(status='Active')
    paginator = Paginator(account_list, 10)
    page_number = request.GET.get('page', 1)
    account = paginator.page(page_number)

    return render(request, 'account_detail.html', {'account': account})
"""
