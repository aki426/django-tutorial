from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
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
    fields = ("title", "text", "category", "thumbnail")
    success_url = reverse_lazy("list-book")


class DeleteBookView(DeleteView):
    template_name = "book/book_confirm_delete.html"
    model = Book
    success_url = reverse_lazy("list-book")


class UpdateBookView(UpdateView):
    template_name = "book/book_update.html"
    model = Book
    fields = ("title", "text", "category", "thumbnail")
    success_url = reverse_lazy("list-book")


class CreateReviewView(CreateView):
    model = Review
    fields = ("book", "title", "text", "rate")
    template_name = "book/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.get(pk=self.kwargs["book_id"])
        print(self.kwargs)
        print(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("detail-book", kwargs={"pk": self.object.book.id})
