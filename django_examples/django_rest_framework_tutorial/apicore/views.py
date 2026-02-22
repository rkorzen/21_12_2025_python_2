from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class APIRoot(APIView):

    def get(self, request):
        data = {
            "users": reverse("user-list", request=request),
            "snippets": reverse("snippet-list", request=request),
            "books": reverse("book-list", request=request)
        }
        return Response(data)
