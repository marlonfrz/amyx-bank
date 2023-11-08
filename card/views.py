from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CardCreateForm, CardEditForm
from .models import Card


# http://dsw.pc16.aula109:8000/create_card
@login_required
def create_card(request):
    if request.method == "POST":
        card_form = CardCreateForm(request.POST)
        if card_form.is_valid():
            new_card = card_form.save()
            Card.objects.create(card_name=new_card)
            # Generar la URL inversa con el valor de id
            url = reverse('card_detail', {'id': new_card.id})
            return redirect(url)
        else:
            return HttpResponse('Formulario invalido')
    else:
        card_form = CardCreateForm()
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


def card_detail(request, card_account_code):
    try:
        card = Card.objects.get(card_account_code=card_account_code)
    except Card.DoesNotExist:
        # Manejar la situación en la que no se encontró ninguna tarjeta
        return render(request, "./account/cards.html", {"message": "La tarjeta no existe"})

    # Procesar y mostrar los detalles de la tarjeta
    return render(request, "card_detail.html", {"card_detail": card})
