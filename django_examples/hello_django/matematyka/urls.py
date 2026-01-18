from django.urls import path

from . import views

urlpatterns = [
    path("<op>/<a>/<b>/", views.calculate, name="home"),

]
