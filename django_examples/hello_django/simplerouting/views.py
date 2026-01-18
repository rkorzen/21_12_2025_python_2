from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello in Django ALX Course")

def hello(request, username=""):
    if username:
        text = f"Hello {username}"
    else:
        text = "Hello World"

    return HttpResponse(text)
