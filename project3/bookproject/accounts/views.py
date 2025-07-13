from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib import messages

from .forms import SignupForm


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("index")


# DjangoのデフォルトLogoutViewがPOSTメソッドのみを受け付けるように設計されているため、
# 関数ベースビューにてGETメソッドを受け付け即座にログアウトする。


def logout_view(request):
    """即座にログアウト"""
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect("index")
