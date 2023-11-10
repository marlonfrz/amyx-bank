from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from amyx_bank.utils import generate_random_code
from account.models import BankAccount, Profile

from .forms import CardCreateForm, CardEditForm
from .models import Card


# http://dsw.pc16.aula109:8000/card/create_card
@login_required
def create_card(request):
    if request.method == "POST":
        card_form = CardCreateForm(request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            user = authenticate(request, username=request.user.username, password=cd["password"])
            print(user.username)
            if user is not None:
                profile = get_object_or_404(Profile, user=user)
                destined_account = cd["accounts"]
                account = BankAccount.objects.filter(profile=profile).get(account_name=destined_account)
                print(account)
                card = card_form.save(commit=False)
                card.account = account
                card.cvc = generate_random_code(3)
                card.save()
                return redirect('dashboard')
            else:
                return HttpResponse('Invalid Credencials')
        else:
            return HttpResponse('Formulario invalido')
    else:
        profile = get_object_or_404(Profile, user=request.user)
        accounts = BankAccount.objects.filter(profile=profile)
        card_form = CardCreateForm(accounts=accounts)
    return render(request, "card/card_create.html", {"card_create_form": card_form})


# http://dsw.pc16.aula109:8000/edit/card/<int:id>/
@login_required
def card_edit(request, id):  # el pk es primarykey
    card_id = Card.objects.get(id=id)
    if request.method == "POST":
        form = CardEditForm(request.POST, instance=card_id)
        if form.is_valid():
            form.save()
            return redirect("card_detail", id=id)
    else:
        form = CardEditForm(instance=card_id)
    return render(request, "card_edit.html", {"card_edit_form": form})


""" @login_required
def card_detail(request, card_account_code):
    card = Card.objects.get(card_account_code=card_account_code)
    return render(request, "card_detail.html", {"card_detail": card_detail}) """


@login_required
def card_detail(request, id):
    card = get_object_or_404(Card, id=id)
    return render(request, "cards/card_detail.html", {"card": card})
