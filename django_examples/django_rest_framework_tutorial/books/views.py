from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
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



@csrf_exempt
def book_detail(request, pk):
    ALLOWED_METHODS = ["GET", "PUT", "DELETE"]

    if request.method not in ALLOWED_METHODS:
        return HttpResponseNotAllowed(ALLOWED_METHODS)

    try:
        snippet = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = BookSerializer(snippet)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BookSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)
