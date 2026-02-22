from django.shortcuts import render

from .models import Snippet
from .serializers import SnippetSerializer
from django.http import JsonResponse
# Create your views here.

# GET /snippets
# POST /snippets
def snippet_list(request):
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return JsonResponse(serializer.data, safe=False)

"""
Content-Type: application/json  # text/html

"""

# GET /snippets/<int:pk>
# PUT /snippets/<int:pk>
# DELETE /snippets/<int:pk>
def snippet_detail(request, pk): ...