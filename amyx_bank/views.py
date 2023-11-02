from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import BankAccountForm, LoginForm, Profile, UserRegistrationForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
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
                    return redirect('dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def bank_account_create_view(request):
    if request.method == 'POST':
        bank_account_form = BankAccountForm(request.POST)
        if bank_account_form.is_valid():
            new_bank_account = bank_account_form.save(commit=False)
            new_bank_account.save()
            # Redirige a la página de inicio del tablero o donde desees después de crear la cuenta
            return redirect('account_create_success')
    else:
        form = BankAccountForm()
    return render(request, 'amyx_bank/account_create.html', {'bank_account_create_form': form})


@login_required
def card_create_view(request):
    pass


@login_required
def edit_account(request):
    pass


@login_required
def edit_card(request):
    pass


def account_create_success(request):
    return render(request, 'amyx_bank/account_create_done.html')


def logout(request):
    return render(request, 'registration/logout.html')


def main(request):
    return render(request, 'amyx_bank/main.html')
