from django.shortcuts import render
from .models import blog
# Create your views here.


def post_list(request):
    return render(request, "blog/list.html", {"posts": blog.posts})


def post_details(request, id):
    post = blog.get_post(id)

    return render(request, "blog/details.html", {"post": post})