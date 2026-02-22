from django.urls import path
from . import views

urlpatterns = [
    path("", views.snippet_list, name="snippet-list"),
    path("<int:pk>/", views.snippet_detail, name="snippet-detail")
]