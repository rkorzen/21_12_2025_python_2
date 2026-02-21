import logging
from django.views.generic import ListView
from django.shortcuts import render
from .services import blog
from .models import Post
# Create your views here.
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)
def post_list(request):

    paginator = Paginator(blog.posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    logger.info(f"Pobieram strone: {page_number} z {paginator.num_pages}")

    return render(request, "blog/list.html", {"page_obj": page_obj})

class PostListView(ListView):
    model = Post
    template_name = "blog/list.html"
    paginate_by = 9

    def get_queryset(self):
        return self.model.objects.filter(is_published=True)

def post_details(request, id):
    post = blog.get_post(id)

    return render(request, "blog/details.html", {"post": post})