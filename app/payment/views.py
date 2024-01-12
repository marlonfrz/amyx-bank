import csv
import json
from decimal import Decimal

import requests
import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from account.models import BankAccount, Profile
from amyx_bank.ourutils import calc_commission, get_bank_info
from card.models import Card
from payment.forms import PaymentForm, TransactionForm

from .models import Payment, Transaction

# from itertools import chain


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
        if not correct_pin:
            return HttpResponseBadRequest("Everything went ok, but you don't have enough money")
        if card.account.balance < taxed_amount:
            return HttpResponseForbidden(f"The code pin {pin} doesn't match")
        card.account.balance -= taxed_amount
        card.account.save()
        new_payment = Payment.objects.create(
            card=card,
            business=business,
            amount=taxed_amount,
        )
        return redirect(reverse("payment_detail", args=[new_payment.id]))
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
        if cac.balance < taxed_amount:
            return HttpResponseBadRequest("You do not have enough money!")
        url = f"{destined_bank}/transfer/incoming/"
        status = requests.post(
            url, json={"sender": sender, "cac": account, "concept": concept, "amount": str(amount)}
        )
        if status.status_code != 200:
            return HttpResponseBadRequest(
                f"The account {account} you tried to send money to does not exist"
            )
        cac.balance -= taxed_amount
        cac.save()
        new_transaction = Transaction.objects.create(
            agent=sender,
            account=account,
            concept=concept,
            amount=taxed_amount,
            kind=Transaction.TransactionType.OUTGOING,
        )
        return redirect(reverse("payments:transaction_detail", args=[new_transaction.id]))
    else:
        form = TransactionForm()
    return render(request, "payment/transactions.html", {"transaction_form": form})


@csrf_exempt
def incoming_transactions(request):
    cd = json.loads(request.body)
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
        amount=total_amount,
        kind=Transaction.TransactionType.INCOMING,
    )
    return redirect(reverse("payments:transaction_detail", args=[new_transaction.id]))


@csrf_exempt
def payroll(request):
    # NOMINA
    # Los campos de payroll son unicamente la cuenta destino y
    # La cantidad de dinero a instroducir
    # cuyos nombres seran cac y balance respectivamente
    cd = json.loads(request.body)
    balance = Decimal(cd.get("balance"))
    account = get_object_or_404(BankAccount, account_code=cd.get("cac").upper())
    account.balance += balance
    account.save()
    return HttpResponse("Payroll done")


@login_required
def movements(request):
    all_movements = []
    profile = get_object_or_404(Profile, user=request.user)
    accounts = profile.accounts.all()
    for account in accounts:
        outgoing_movements = Transaction.objects.filter(
            agent__icontains=account.account_code, kind=Transaction.TransactionType.OUTGOING
        )
        incoming_movements = Transaction.objects.filter(
            account__icontains=account.account_code, kind=Transaction.TransactionType.INCOMING
        )
        all_movements.extend(outgoing_movements)
        all_movements.extend(incoming_movements)
        for card in account.cards.all():
            if payments := card.payments.all():
                all_movements.extend(payments)
    all_movements = sorted(all_movements, key=lambda instance: instance.timestamp, reverse=True)
    return render(request, "payment/movements.html", {"payments": all_movements})


# PDF TO FIX
@staff_member_required
def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    html = render_to_string("templates/payment/transaction_pdf.html", {"transaction": transaction})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=transaction_{transaction.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "static/css/base.css")]
    )
    return response


# PDF TO FIX ---- hacer comando python manage.py collectstatic, si no funciona sergio tiene otra solución en su codigo final ----
@staff_member_required
def payment_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    html = render_to_string("templates/payment/payment_pdf.html", {"payment": payment})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=payment_{payment.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(
        response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "static/css/base.css")]
    )
    return response


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


def prueba(request):
    profile = get_object_or_404(Profile, user=request.user)
    accounts = []
    for account in profile.accounts.all():
        accounts.append(account)
    accounts2 = list(profile.accounts.all())
    cards = list(accounts2[0].cards.all())
    print(accounts2[0].cards.all())
    return HttpResponse(f"Perfil: {profile}, Cuentas: {accounts2}, Tarjetas: {cards}, Pagos")
