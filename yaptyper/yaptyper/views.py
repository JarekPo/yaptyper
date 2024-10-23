import os
import sys
from django.shortcuts import redirect, render
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from app_version import __version__


class LoginView(auth_views.LoginView):
    template_name = "auth/login.html"


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "auth/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def home(request):
    return render(request, "home.html", {"version": __version__})
