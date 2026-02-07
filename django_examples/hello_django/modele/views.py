from django.shortcuts import render
from .models import Instructor
# Create your views here.
def instructor_detail(request, id):
    i = Instructor.objects.get(id=id)
    return render(request, 'models/instructor_detail.html', {'instructor': i})