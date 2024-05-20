from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("about_us/", views.about_us, name="about_us"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path("edit/profile/", views.edit_profile, name="edit_profile"),
    # path('inicio/', views.inicio, name='inicio'),
    # path('detalle/<int:id>/', views.detalle, name='detalle'),
]
