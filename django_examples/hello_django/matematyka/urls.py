from django.urls import path

from . import views

app_name = "mathematics"
urlpatterns = [
    path("<op>/<a>/<b>/", views.calculate, name="home"),

]
