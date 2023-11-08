from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from account.forms import UserRegistrationForm
from account.models import Profile

from .forms import AccountEditForm, AccountForm, LoginForm, ProfileForm
from .models import BankAccount


# http://dsw.pc16.aula109:8000/
# http://dsw.pc16.aula109:8000/
def main(request):
    return render(request, "amyx_bank/main.html")


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


# http://dsw.pc16.aula109:8000/register
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


# http://dsw.pc16.aula109:8000/login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "account/dashboard.html", {"section": "dashboard"})
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


# http://dsw.pc16.aula109:8000/logout
def log_out(request):
    logout(request)
    return render(request, "registration/logout.html")


# http://dsw.pc16.aula109:8000/create_account
@login_required
def bank_account_create_view(request):
    if request.method == "POST":
        bank_account_form = AccountForm(request.POST)
        if bank_account_form.is_valid():
            bank_account_form.save()
            return redirect("dashboard")
    else:
        form = AccountForm()
    return render(request, "account/account_create.html", {"bank_account_create_form": form})


# http://dsw.pc16.aula109:8000/edit/account/<int:id>/
@login_required
def edit_bank_account(request, id):  # el pk es primarykey
    bank_account = BankAccount.objects.get(id=id)
    if request.method == "POST":
        form = AccountEditForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            return render(request, "bank_account_detail", id=id)
    else:
        form = AccountEditForm(instance=bank_account)
    return render(request, "edit_bank_account.html", {"account_edit_form": form})


# def inicio(request):
#    return HttpResponse("Esta es la página de inicio. <a href='" + reverse('detalle', args=[1]) + "'>Ir a Detalle</a>")

# def detalle(request, id):
#    return HttpResponse("Detalles del elemento #" + str(id))


def account_detail(request, id):
    account = get_object_or_404(BankAccount, id=id)
    return render(request, 'account/account_detail.html', {"account": account})
