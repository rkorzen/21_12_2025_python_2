from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("hello/", views.hello, name="hello"),
    path("hello/<username>", views.hello, name="hello_username")
]
