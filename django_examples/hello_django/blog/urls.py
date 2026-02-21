from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("posts/<int:id>", views.PostDetailView.as_view(), name="details"),

]