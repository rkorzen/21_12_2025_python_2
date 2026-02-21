from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.BookListView.as_view(), name="list"),
    path("create/", views.BookCreateView.as_view(), name="create"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="details"),
]