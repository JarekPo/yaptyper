import os
import sys
from django.shortcuts import redirect, render
from django.contrib.auth import login, views as auth_views, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.models import User

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

class GuestLoginView(View):
    template_name = "auth/guest_login.html"
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        guest_name = request.POST.get("guest_name")
        if not guest_name:
            return render(request, self.template_name, {"error": "Guest name is required"})
        username = f"{guest_name} (guest)"
        password = "default_guest_password"
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.isGuest = True
            user.save()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            request.session["isGuest"] = True
            return redirect("home")

        return render(request, self.template_name, {"error": "Unable to log in as guest"})


def home(request):
    return render(request, "home.html", {"version": __version__})
