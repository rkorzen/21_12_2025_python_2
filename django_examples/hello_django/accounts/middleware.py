from django.conf import settings

class DebugRequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            print(f"Request: {request.method}{request.path}")
            print(f"Headers: {request.headers}")
            print(f"Body: {request.body}")
            print(f"Cookies: {request.COOKIES}")
            print(f"Cookies: {request.POST}")

        response = self.get_response(request)

        if settings.DEBUG:
            print(f"Response: {request.method} {request.path} -> {response.status_code}")
        return response