from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from amyx_bank.forms import (
    LoginForm,
    ProfileEditForm,
    ProfileForm,
    UserEditForm,
    UserRegistrationForm,
)

from amyx_bank.models import Profile


# http://dsw.pc16.aula109:8000/
def main(request):
    return render(request, "amyx_bank/main.html")


# http://dsw.pc16.aula109:8000/register
def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return render(request, "registration/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "registration/register.html", {"user_form": user_form})


# http://dsw.pc16.aula109:8000/login
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "account/dashboard.html", {"section": "dashboard"})
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


# http://dsw.pc16.aula109:8000/logout
@login_required
def log_out(request):
    logout(request)
    return render(request, "registration/logout.html")


# http://dsw.pc16.aula109:8000/account/edit/profile
@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=get_object_or_404(Profile, user=request.user), files=request.FILES)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect("dashboard")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=get_object_or_404(Profile, user=request.user))
    return render(
        request,
        "account/edit_profile.html",
        {"user_edit_form": user_form, "profile_edit_form": profile_form},
    )


def about_us(request):
    return render(request, "amyx_bank/about_us.html")



# def inicio(request):
#    return HttpResponse("Esta es la página de inicio. <a href='" + reverse('detalle', args=[1]) + "'>Ir a Detalle</a>")

# def detalle(request, id):
#    return HttpResponse("Detalles del elemento #" + str(id))
