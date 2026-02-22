from django.urls import path
from . import views

urlpatterns = [
    path("", views.snippet_list, name="snippet-list")
]