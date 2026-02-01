from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="list"),
    path("posts/<int:id>", views.post_details, name="list"),

]