from rest_framework import permissions
from rest_framework import viewsets

from books.models import Book
from .serializers import BookSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
