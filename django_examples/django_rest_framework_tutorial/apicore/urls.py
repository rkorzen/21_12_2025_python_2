from django.urls import path
from . import views

urlpatterns = [
    path("", views.APIRoot.as_view(), name="api-root"),
]