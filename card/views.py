from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from account.models import BankAccount, Profile
from amyx_bank.utils import generate_random_code

from .forms import CardCreateForm, CardEditForm
from .models import Card


# http://dsw.pc16.aula109:8000/card/create_card
@login_required
def create_card(request):
    if request.method == "POST":
        profile = get_object_or_404(Profile, user=request.user)
        card_form = CardCreateForm(profile, request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            user = authenticate(request, username=request.user.username, password=cd["password"])
            if user is not None:
                destined_account = cd["accounts"]
                account = BankAccount.objects.filter(profile=profile).get(
                    account_name=destined_account
                )
                card = card_form.save(commit=False)
                card.account = account
                cvc = generate_random_code(3)
                send_mail(
                    'You card\'s CVC',  # Email concept
                    f"""Your card {card} has been created succesfully.
                        Your card's CVC is: {cvc}.
                        Remember or keep this code for your activities.


                        This email has been generated automatically and is for educational purposes from students of IES Puerto de la Cruz.
                        We are sorry if you receive this by our testing and we appologise for it, you are very welcome to mark us as spam.""",  # Email Message
                    f'{settings.EMAIL_HOST_USER}',  # Email sender
                    [user.email],  # Email receiver
                    fail_silently=True,  # So the server does not crash
                )
                card.cvc = make_password(cvc)
                card.save()
                return redirect('dashboard')
            else:
                return HttpResponse('Invalid Credencials')
        else:
            return HttpResponse('Formulario invalido')
    else:
        profile = get_object_or_404(Profile, user=request.user)
        card_form = CardCreateForm(profile)
    return render(request, "card/card_create.html", {"card_create_form": card_form})


# http://dsw.pc16.aula109:8000/edit/card/<int:id>/
@login_required
def card_edit(request, id):
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
