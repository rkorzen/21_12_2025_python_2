from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookList.as_view(), name="book-list"),
    path("<int:pk>", views.BookDetail.as_view(), name="book-detail"),
]
