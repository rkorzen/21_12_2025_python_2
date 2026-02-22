from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Snippet
from .serializers import SnippetSerializer


# Create your views here.

# GET /snippets
# POST /snippets
class SnippetList(APIView):

    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
Content-Type: application/json  # text/html

"""


# GET /snippets/<int:pk>
# PUT /snippets/<int:pk>
# DELETE /snippets/<int:pk>
class SnippetDetail(APIView):

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        serializer = SnippetSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        snippet = self.get_object(pk)
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
