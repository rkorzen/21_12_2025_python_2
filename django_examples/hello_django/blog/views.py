from django.shortcuts import render
from .models import blog
# Create your views here.
from django.core.paginator import Paginator

def post_list(request):

    paginator = Paginator(blog.posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/list.html", {"page_obj": page_obj})


def post_details(request, id):
    post = blog.get_post(id)

    return render(request, "blog/details.html", {"post": post})