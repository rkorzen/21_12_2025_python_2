from django.urls import path
from rest_framework import renderers

from . import views


user_list = views.UserViewSet.as_view({"get": "list"})
user_detail = views.UserViewSet.as_view({"get": "retrieve"})

snippets_list = views.SnippetViewSet.as_view({"get": "list", "post": "create"})
snippets_detail = views.SnippetViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
snippets_highlight = views.SnippetViewSet.as_view({"get": "highlight"}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = [

    path("snippets/", snippets_list, name="snippet-list"),
    path("snippets/<int:pk>/", snippets_detail, name="snippet-detail"),
    path("snippets/<int:pk>/highlight/", snippets_highlight, name="snippet-highlight"),
    path("users/", user_list, name="user-list"),
    path("users/<int:pk>/", user_detail, name="user-detail"),


]