from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = (
            'url', 'id', 'title', 'author', 'status', 'visible', 'created'  # __all__
        )
