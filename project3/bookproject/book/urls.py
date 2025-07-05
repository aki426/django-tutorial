from django.urls import path

from . import views

urlpatterns = [
    path("book/", views.ListBookView.as_view())
]
