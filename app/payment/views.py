import csv
import json
from decimal import Decimal
from io import StringIO

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML

from account.models import BankAccount, Profile
from amyx_bank.ourutils import calc_commission, get_bank_info
from card.models import Card
from payment.forms import PaymentForm, TransactionForm

from .models import Payment, Transaction


@login_required
@csrf_exempt
def payment(request):
    profile = get_object_or_404(Profile, user=request.user)
    accounts = profile.accounts.all()
    if request.method == "POST":
        try:
            cd = json.loads(request.body)
        except json.JSONDecodeError:
            form = PaymentForm(accounts, request.POST)
            if form.is_valid():
                cd = form.cleaned_data
        else:
            return HttpResponseBadRequest(
                "Payment was cancelled due to invalid information passed in the POST request"
            )
        business = cd.get("business").upper()
        card = cd.get("ccc")
        amount = Decimal(cd.get("amount"))
        if amount == 0:
            return HttpResponseBadRequest("You cannot send no money to anyone!")
        pin = cd.get("pin")
        correct_pin = check_password(pin, card.cvc)
        taxed_amount = amount + calc_commission(amount, "PAYMENTS")
        if not correct_pin:
            return HttpResponseForbidden(f"The code pin {pin} doesn't match")
        if card.account.balance < taxed_amount:
            return HttpResponseBadRequest("Everything went ok, but you don't have enough money")
        card.account.balance -= taxed_amount
        card.account.save()
        new_payment = Payment.objects.create(
            card=card,
            business=business,
            amount=taxed_amount,
        )
        return redirect(reverse("payments:payment_detail", args=[new_payment.id]))
    else:
        form = PaymentForm(accounts)
    return render(request, "payment/payment.html", {"payment_form": form})


@login_required
@csrf_exempt
def outgoing_transactions(request):
    # Este bloque controla que los datos pueden
    # llegar tanto por formulario como por curl
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        try:
            cd = json.loads(request.body)
        except json.JSONDecodeError:
            form = TransactionForm(profile, request.POST)
            if form.is_valid():
                cd = form.cleaned_data
        else:
            return HttpResponseBadRequest(
                "Transaction was cancelled due to invalid information passed in the POST request"
            )
        # Obtención los datos del diccionario
        sender = cd.get("sender")
        account = cd.get("cac").upper()
        # Clausulas guarda para despachar los errores posibles
        if sender.account_code == account:
            return HttpResponse("You can't send money to yourself")
        amount = Decimal(cd.get("amount"))
        if amount == 0:
            return HttpResponse("You can't send no money to anyone")
        concept = cd.get("concept")
        destined_bank = get_bank_info(account, "url")
        taxed_amount = amount + calc_commission(amount, "OUTGOING")
        if sender.balance < taxed_amount:
            return HttpResponseBadRequest("You do not have enough money!")
        url = f"{destined_bank}/{request.LANGUAGE_CODE}/transfer/incoming/"
        status = requests.post(
            url, json={"sender": sender.account_code, "cac": account, "concept": concept, "amount": str(amount)}
        )
        if status.status_code != 200:
            return HttpResponseBadRequest(
                f"The account {account} you tried to send money to does not exist"
            )
        sender.balance -= taxed_amount
        sender.save()
        new_transaction = Transaction.objects.create(
            agent=sender,
            account=account,
            concept=concept,
            amount=taxed_amount,
            kind=Transaction.TransactionType.OUTGOING,
        )
        return redirect(reverse("payments:transaction_detail", args=[new_transaction.id]))
    else:
        form = TransactionForm(profile)
    return render(request, "payment/transactions.html", {"transaction_form": form})

@login_required
@csrf_exempt
def incoming_transactions(request):
    cd = json.loads(request.body)
    sender = cd.get("sender").upper()
    cac = cd.get("cac").upper()
    concept = cd.get("concept")
    amount = Decimal(cd.get("amount"))
    # Comprueba que la cuenta existe
    try:
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
    return HttpResponse("Payroll done!")


"""
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

"""

@login_required
def transaction_list(request):
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
    all_movements = sorted(all_movements, key=lambda instance: instance.timestamp, reverse=True)
    movements_per_page = 5
    paginator = Paginator(all_movements, movements_per_page)
    page = request.GET.get('page')
    try:
        movements_page = paginator.page(page)
    except PageNotAnInteger:
        movements_page = paginator.page(1)
    except EmptyPage:
        movements_page = paginator.page(paginator.num_pages)
    return render(request, "payment/movements.html", {"payments": movements_page})


@login_required
def payment_list(request):
    all_movements = []
    profile = get_object_or_404(Profile, user=request.user)
    accounts = profile.accounts.all()
    for account in accounts:
        for card in account.cards.all():
            if payments := card.payments.all():
                all_movements.extend(payments)
    all_movements = sorted(all_movements, key=lambda instance: instance.timestamp, reverse=True)
    movements_per_page = 5
    paginator = Paginator(all_movements, movements_per_page)
    page = request.GET.get('page')
    try:
        movements_page = paginator.page(page)
    except PageNotAnInteger:
        movements_page = paginator.page(1)
    except EmptyPage:
        movements_page = paginator.page(paginator.num_pages)
    return render(request, "payment/movements.html", {"payments": movements_page})


@login_required
def export_csv(request):
    movements = request.POST.getlist("selected_elements")
    payments = []
    transactions = []
    for movement in movements:
        movement_id, movement_type = movement.split("-")
        if eval(movement_type) == Transaction:
            transactions.append(Transaction.objects.get(id=movement_id))
        if eval(movement_type) == Payment:
            payments.append(Payment.objects.get(id=movement_id))
    response = HttpResponse(content_type='text/csv')
    if payments:
        response['Content-Disposition'] = 'attachment; filename=payments.csv'
        with StringIO() as payments_csv_file:
            file_writer = csv.writer(payments_csv_file)
            file_writer.writerow(["id", "Card", "Business", "Amount", "Kind", "Timestamp"])
            for payment in payments:
                file_writer.writerow(
                    [
                        payment.id,
                        payment.card,
                        payment.business,
                        payment.amount,
                        payment.kind,
                        payment.timestamp,
                    ]
                )
            response.write(payments_csv_file.getvalue())
    if transactions:
        response['Content-Disposition'] = 'attachment; filename=transactions.csv'
        with StringIO() as transactions_csv_file:
            file_writer = csv.writer(transactions_csv_file)
            file_writer.writerow(["id", "Agent", "Account", "Amount", "Kind", "Timestamp"])
            for transaction in transactions:
                file_writer.writerow(
                    [
                        transaction.id,
                        transaction.agent,
                        transaction.account,
                        transaction.amount,
                        transaction.kind,
                        transaction.timestamp,
                    ]
                )
            response.write(transactions_csv_file.getvalue())
    if not any([payments, transactions]):
        return HttpResponse("You have not selected any transaction or payment!")
    return response


@login_required
def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    html = render_to_string("payment/transaction_pdf.html", {"transaction": transaction})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={transaction.id}.pdf"
    HTML(string=html).write_pdf(response)
    return response


@login_required
def payment_pdf(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    html = render_to_string("payment/payment_pdf.html", {"payment": payment})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename={payment.id}.pdf'
    # f'attachment; filename="{document.title}.pdf"'
    HTML(string=html).write_pdf(response)
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
