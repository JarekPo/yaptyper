from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class LoginView(auth_views.LoginView):
    template_name = "auth/login.html"


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "auth/register.html"


def home(request):
    return render(request, "home.html")
