from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("hello/", views.hello, name="hello"),
    path("hello/<username>", views.hello, name="hello_username"),
    path("hello2/", views.HelloView.as_view(), name="hello2"),
    path("hello2/<username>", views.HelloView.as_view(), name="hello2_username"),
]
