from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Book, Review


def index_view(request):
    object_list = Book.objects.all().order_by("category")
    return render(request, "book/index.html", {"object_list": object_list})


class ListBookView(ListView):
    template_name = "book/book_list.html"
    model = Book


class DetailBookView(DetailView):
    template_name = "book/book_detail.html"
    model = Book


class CreateBookView(CreateView):
    template_name = "book/book_create.html"
    model = Book
    fields = ("title", "text", "category")
    success_url = reverse_lazy("list-book")


class DeleteBookView(DeleteView):
    template_name = "book/book_confirm_delete.html"
    model = Book
    success_url = reverse_lazy("list-book")


class UpdateBookView(UpdateView):
    template_name = "book/book_update.html"
    model = Book
    fields = ("title", "text", "category")
    success_url = reverse_lazy("list-book")


class CreateReviewView(CreateView):
    model = Review
    fields = ("book", "title", "text", "rate")
    template_name = "book/review_form.html"
