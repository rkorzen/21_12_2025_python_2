from django.shortcuts import render
from .models import Instructor
from .forms import DepartmentForm


# Create your views here.
def instructor_detail(request, id):
    i = Instructor.objects.get(id=id)
    return render(request, 'models/instructor_detail.html', {'instructor': i})


def department_create(request):

    if request.method == "POST":
        form = DepartmentForm(data=request.POST)
        if form.is_valid():
            form.save()
            print("Powiodlo sie")



    form = DepartmentForm()
    return render(
        request,
        "models/department_form.html",
        {"form": form}
    )
