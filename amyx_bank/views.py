from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import BankAccount
from .forms import AccountEditForm, LoginForm

from account.forms import UserRegistrationForm
from account.models import Profile


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
                    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
    
def logout(request):
    return render(request, 'registration/logout.html')


@login_required
def main(request):
    return render(request, 'amyx_bank/main.html')

@login_required
def edit_bank_account(request, pk): #el pk es primarykey
    bank_account = BankAccount.objects.get(pk=pk)
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance=bank_account)
        if form.is_valid():
            form.save()
            return redirect('bank_account_detail', pk=pk)
    else:
        form = AccountEditForm(instance=bank_account)
    return render(request, 'edit_bank_account.html', {'account_edit_form':form})
