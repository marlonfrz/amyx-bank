from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import check_password, make_password
from .forms import PaymentForm
from django.http import HttpResponse, HttpResponseForbidden
from card.models import Card
from account.models import BankAccount, Profile
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

#data = {'nombre': request.POST['nombre'], 'apellido': request.POST['apellido']} con los datos de la operacion
#response = requests.post('http://ejemplo.com/api/endpoint', data=data)

@csrf_exempt
def payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
        except json.JSONDecodeError:
            form = PaymentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                business = cd.get('business')
                ccc = cd.get('ccc')
                amount = cd.get('amount')
                pin = cd.get('pin')
                try:
                    card = Card.objects.get(card_code=ccc)
                    correct_pin = check_password(card.cvc, make_password(pin))
                    print(correct_pin)
                    balance = card.account.balance
                    if correct_pin:
                        if balance > amount:
                            balance -= amount
                            return HttpResponse("Ok!")
                        else:
                            return HttpResponse(status=403)
                    else:
                        return HttpResponseForbidden("the code pin doesn't match")
                except Card.DoesNotExist:
                    return HttpResponseForbidden(f"Card {ccc} doesn't exists")
            print("pepe")
    else:
        form = PaymentForm()
    return render(request, 'payment/payment.html', {'payment_form' : form})

@login_required
def transactions(request):
    pass

@login_required
def transfer(request):
    pass

@login_required
def commissions(request):
    pass

@login_required
def buy(request):
    pass

@login_required
def payment_success(request):
    return redirect("dashboard")
