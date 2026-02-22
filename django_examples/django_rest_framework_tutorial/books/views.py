from django.http import JsonResponse, HttpResponseNotAllowed
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from books.models import Book
from .serializers import BookSerializer

# Create your views here.

@csrf_exempt
def book_list(request):
    ALLOWED_METHODS = ["GET", "POST"]

    if request.method not in ALLOWED_METHODS:
        return HttpResponseNotAllowed(ALLOWED_METHODS)

    if request.method == "GET":
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
