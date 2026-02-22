from django.http import JsonResponse

from books.models import Book
from .serializers import BookSerializer

# Create your views here.

def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return JsonResponse(serializer.data, safe=False)
