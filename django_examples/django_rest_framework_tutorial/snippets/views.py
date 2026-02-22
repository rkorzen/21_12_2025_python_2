from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetSerializer
from django.http import JsonResponse, HttpResponseNotAllowed


# Create your views here.

# GET /snippets
# POST /snippets
@csrf_exempt
def snippet_list(request):
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    return HttpResponseNotAllowed(["GET", "POST"])

"""
Content-Type: application/json  # text/html

"""

# GET /snippets/<int:pk>
# PUT /snippets/<int:pk>
# DELETE /snippets/<int:pk>
def snippet_detail(request, pk): ...