from django.shortcuts import render

def _reports_cards():
    return {}

# Create your views here.
def reports_home(request):
    return render(
        request,
        "reporting/reports_home.html", {"reports": _reports_cards()}
    )