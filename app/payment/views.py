import json
from decimal import Decimal
from itertools import chain

import requests
from account.models import BankAccount
from amyx_bank.ourutils import calc_commission, get_bank_info
from card.models import Card
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from payment.forms import PaymentForm, TransactionForm

from .models import Payment, Transaction


@csrf_exempt
def payment(request):
    if request.method == "POST":
        try:
            cd = json.loads(request.body)
        except json.JSONDecodeError:
            form = PaymentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
        else:
            return HttpResponseBadRequest(
                "Payment was cancelled due to invalid information passed in the POST request"
            )
        business = cd.get("business").upper()
        ccc = cd.get("ccc").upper()
        amount = Decimal(cd.get("amount"))
        if amount == 0:
            return HttpResponseBadRequest("You cannot send no money to anyone!")
        pin = cd.get("pin")
        try:
            card = Card.objects.get(card_code=ccc)
        except Card.DoesNotExist:
            return HttpResponseForbidden(f"Card {ccc} doesn't exists")
        correct_pin = check_password(pin, card.cvc)
        taxed_amount = amount + calc_commission(amount, "PAYMENTS")
        if correct_pin:
            if card.account.balance > taxed_amount:
                card.account.balance -= taxed_amount
                card.account.save()
                new_payment = Payment.objects.create(
                    card=card,
                    business=business,
                    amount=amount,
                )
                return redirect(reverse("payment_detail", args=[new_payment.id]))
            else:
                return HttpResponseBadRequest("Everything went ok, but you don't have enough money")
        else:
            return HttpResponseForbidden(f"The code pin {pin} doesn't match")
    else:
        form = PaymentForm()
    return render(request, "payment/payment.html", {"payment_form": form})


@login_required
@csrf_exempt
def outgoing_transactions(request):
    # Este bloque controla que los datos pueden
    # llegar tanto por formulario como por curl
    if request.method == "POST":
        try:
            cd = json.loads(request.body)
        except json.JSONDecodeError:
            form = TransactionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
        else:
            return HttpResponseBadRequest(
                "Transaction was cancelled due to invalid information passed in the POST request"
            )
        # Obtención los datos del diccionario
        sender = cd.get("sender").upper()
        account = cd.get("cac").upper()
        # Clausulas guarda para despachar los errores posibles
        if sender == account:
            return HttpResponse("You can't send money to yourself")
        amount = Decimal(cd.get("amount"))
        if amount == 0:
            return HttpResponse("You can't send no money to anyone")
        concept = cd.get("concept")
        destined_bank = get_bank_info(account, "url")
        # Obtiene la cuenta del sender
        try:
            cac = BankAccount.objects.get(account_code=sender)
        except BankAccount.DoesNotExist:
            return HttpResponseForbidden(f"Account {sender} doesn't exists")
        taxed_amount = amount + calc_commission(amount, "OUTGOING")
        if cac.balance > taxed_amount:
            url = f"{destined_bank}:8000/transfer/incoming/"
            print(url)
            transaction = {
                "sender": sender,
                "cac": account,
                "concept": concept,
                "amount": str(amount),
            }
            status = requests.post(url, json=transaction)
            print(status.status_code)
            if status.status_code == 200:
                cac.balance -= taxed_amount
                cac.save()
                new_transaction = Transaction.objects.create(
                    agent=sender,
                    account=account,
                    concept=concept,
                    amount=amount,
                    kind=Transaction.TransactionType.OUTGOING,
                )
                return redirect(reverse("transaction_detail", args=[new_transaction.id]))
            else:
                return HttpResponseBadRequest(
                    f"The account {account} you tried to send money to does not exist"
                )
        else:
            return HttpResponseBadRequest("You do not have enough money!")
    else:
        form = TransactionForm()
    return render(request, "payment/transactions.html", {"transaction_form": form})


@csrf_exempt
def incoming_transactions(request):
    # Este bloque controla que los datos pueden
    # llegar tanto por formulario como por curl
    # Puede llegar la solicitud mediante curl
    cd = json.loads(request.body)
    # Obtención los datos del diccionario
    sender = cd.get("sender").upper()
    cac = cd.get("cac").upper()
    concept = cd.get("concept")
    amount = Decimal(cd.get("amount"))
    # Comprueba que la cuenta existe
    try:
        # account = get_object_or_404(BankAccount, account_code=cac)
        account = BankAccount.objects.get(account_code=cac)
    except BankAccount.DoesNotExist:
        return HttpResponseBadRequest(
            f"The account {cac} you tried to send money to does not exist"
        )
    taxed_amount = calc_commission(amount, "INCOMING")
    total_amount = amount - taxed_amount
    account.balance += total_amount
    account.save()
    new_transaction = Transaction.objects.create(
        agent=sender,
        account=cac,
        concept=concept,
        amount=amount,
        kind=Transaction.TransactionType.INCOMING,
    )
    return redirect(reverse("transaction_detail", args=[new_transaction.id]))


@csrf_exempt
def payroll(request):
    # NOMINA
    # Los campos de payroll son unicamente la cuenta destino y
    # La cantidad de dinero a instroducir
    # cuyos nombres seran cac y balance respectivamente
    cd = json.loads(request.body)
    balance = Decimal(cd.get('balance'))
    account = get_object_or_404(BankAccount, account_code=cd.get('cac').upper())
    account.balance += balance
    account.save()
    return HttpResponse("Payroll done")


@login_required
def movements(request):
    transactions = Transaction.objects.all()
    payments = Payment.objects.all()
    all_movements = sorted(
        chain(transactions, payments),
        key=lambda instance: instance.timestamp,
        reverse=True,
    )
    movements_per_page = 5
    paginator = Paginator(all_movements, movements_per_page)
    page = request.GET.get('page')
    try:
        movements_page = paginator.page(page)
    except PageNotAnInteger:
        movements_page = paginator.page(1)
    except EmptyPage:
        movements_page = paginator.page(paginator.num_pages)
    return render(request, "payment/movements.html", {"movements": movements_page})


@login_required
def payment_detail(request, id):
    movement = get_object_or_404(Payment, id=id)
    return render(request, "payment/payment_detail.html", {"movement": movement})


@login_required
def transaction_detail(request, id):
    movement = get_object_or_404(Transaction, id=id)
    return render(request, "payment/transaction_detail.html", {"movement": movement})


@login_required
def payment_success(request):
    return redirect("dashboard")
