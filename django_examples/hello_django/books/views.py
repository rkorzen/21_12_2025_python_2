from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Book

class BookListView(ListView):
    model = Book


class BookDetailView(DetailView):
    model = Book

class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "published_year", "is_avilable"]
    success_url = reverse_lazy("books:list")