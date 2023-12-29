from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path(_("about_us/"), views.about_us, name="about_us"),
    path(_("login/"), views.user_login, name="login"),
    path(_("logout/"), views.log_out, name="logout"),
    path(_("register/"), views.register, name="register"),
    path(_("edit/profile/"), views.edit_profile, name="edit_profile"),
    # path('inicio/', views.inicio, name='inicio'),
    # path('detalle/<int:id>/', views.detalle, name='detalle'),
]
