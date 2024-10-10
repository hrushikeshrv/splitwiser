from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import RegistrationForm
from users.models import User


class UserCreateView(CreateView):
    template_name = "users/register.html"
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)
