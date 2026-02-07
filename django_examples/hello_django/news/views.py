from django.shortcuts import render
from .services import service
# Create your views here.
def news_list(request):
    return render(request, 'news/list.html', {'news': service.get_news()})

def news_detail(request, pk):
    return render(request, 'news/detail.html', {'news': service.get_by_id(pk)})