from rest_framework import generics
from rest_framework import mixins

from .models import Snippet
from .serializers import SnippetSerializer


# Create your views here.

# GET /snippets
# POST /snippets
class SnippetList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


"""
Content-Type: application/json  # text/html

"""


# GET /snippets/<int:pk>
# PUT /snippets/<int:pk>
# DELETE /snippets/<int:pk>
# noinspection PyStubPackagesAdvertiser
class SnippetDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
