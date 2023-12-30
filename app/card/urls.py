from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path(_("cards"), views.cards, name="cards"),
    path(_("create_card/"), views.create_card, name="create_card"),
    path(_("edit/card/<int:id>/"), views.card_edit, name="card_edit"),
    path(_("card_detail/<int:id>/"), views.card_detail, name="card_detail"),
]
