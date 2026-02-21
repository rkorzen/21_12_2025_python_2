from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from .models import HelloUserNameHistory
def index(request):
    return render(
        request,
        "simplerouting/index.html",
        {"text": "Hello in Django ALX Course"}
    )

@csrf_exempt
def hello(request, username="World"):
    if request.method == "GET":
        if not username == "World":
            HelloUserNameHistory(username=username).save()
        return HttpResponse(f"Hello {username}")
    elif request.method == "POST":
        return HttpResponse("Zapytanie POST")


@method_decorator(csrf_exempt, name="dispatch")
class HelloView(View):
    def get(self, request, username="World"):
        if not username == "World":
            HelloUserNameHistory(username=username).save()
        return HttpResponse(f"Hello {username}")


    def post(self, request):
        return HttpResponse("Zapytanie POST")