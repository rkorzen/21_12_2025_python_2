from django.urls import path

from . import views
urlpatterns = [
    path("example/", views.example, name="example")
]