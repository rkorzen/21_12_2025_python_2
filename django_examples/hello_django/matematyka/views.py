from django.shortcuts import render
from django.http import HttpResponse

from matematyka.services import MathService
from . import models

# Create your views here.
def calculate(request, op, a, b):
    result = MathService.calculate(op, int(a), int(b))
    user = request.user if request.user.is_authenticated else None
    models.CalculationHistory.objects.create(
        operation=op,
        a=a,
        b=b,
        result=result,
        user=user
    )


    return render(
        request,
        "matematyka/result.html",
        {"result": result}
        )