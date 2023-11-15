from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password
from .forms import PaymentForm, TransactionForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from card.models import Card
from account.models import BankAccount, Profile
from .models import Payment, Transaction
from django.shortcuts import get_object_or_404
from amyx_bank.ourutils import calc_commission, get_bank_info
import json, requests
from decimal import Decimal
from itertools import chain


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
                card.save()
                card.account.save()
                Payment.objects.create(
                    card=card,
                    business=business,
                    amount=amount,
                )
                return HttpResponse("Ok!")
            else:
                return HttpResponseBadRequest(
                    "Everything went ok, but you don't have enough money"
                )
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
        print(taxed_amount)
        if cac.balance > taxed_amount:
            transaction = {"agent" : sender, "cac" : account, "concept" : concept, "amount" : amount}
            status = requests.post(f"http://127.0.0.1:8000/incoming/", transaction)
            # print(status)
            cac.balance -= taxed_amount
            cac.save()
            Transaction.objects.create(
                agent=sender,
                account=account,
                concept=concept,
                amount=amount,
            )
            return HttpResponse("Everything went ok with the transaction")
        return HttpResponse(
            "todo ha ido bien, solo falta que implementes las nominas"
        )  # QUITAR CUANDO TODO FUNCIONE
    else:
        form = TransactionForm()
    return render(request, "payment/transactions.html", {"transaction_form": form})



@require_POST
def incoming_transactions(request):
    # Este bloque controla que los datos pueden
    # llegar tanto por formulario como por curl
    try:
        cd = json.loads(request.body)
    except json.JSONDecodeError:
        form = TransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        else:
            return HttpResponse("Invalid form data format")

        # Obtención los datos del diccionario
        sender = cd.get("sender")
        cac = cd.get("cac")
        concept = cd.get("concept")
        amount = Decimal(cd.get("amount"))

        # Comprueba que la cuenta existe
        try:
            account = BankAccount.objects.get(account_code=cac)
        except BankAccount.DoesNotExist:
            return HttpResponseBadRequest(
                "The account you tried to send money to does not exist"
            )

        taxed_amount = calc_commission(amount, "INCOMING")
        total_amount = amount - taxed_amount
        account.balance += total_amount
        account.save()
        new_transaction = Transaction.objects.create(
            agent=sender, account=account, concept=concept, amount=amount
        )
        return redirect("dashboard")


@csrf_exempt
def payroll(request):
    # Los campos de payroll son unicamente la cuenta destino y
    # La cantidad de dinero a instroducir
    # cuyos nombres seran cac y balance respectivamente
    cd = json.loads(request.body)
    balance = Decimal((cd.get('balance')))
    account = get_object_or_404(BankAccount, account_code=cd.get('cac').upper())
    account.balance += balance
    account.save()
    return HttpResponse("NOMINA BIEN METIDA PARA DENTRO")


def movements(request):
    transactions = Transaction.objects.all()
    payments = Payment.objects.all()
    all_movements = sorted(
        chain(transactions, payments),
        key=lambda instance: instance.timestamp,
        reverse=True,
    )
    return render(request, "movements.html", {"all_movements": all_movements})


# arreglar esta view


@login_required
def payment_success(request):
    return redirect("dashboard")
