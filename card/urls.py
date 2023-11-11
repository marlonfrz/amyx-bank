from django.urls import path

from . import views

urlpatterns = [
    path("cards", views.cards, name="cards"),
    path("create_card/", views.create_card, name="create_card"),
    path("edit/card/<int:id>/", views.card_edit, name="card_edit"),
    path("card_detail/<int:id>/", views.card_detail, name="card_detail"),
]
