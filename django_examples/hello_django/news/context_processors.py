from news.models import Author, News


def my_context(request):
    return {
        "redakcja": "alx.pl",
        "authors_count": Author.objects.count(),
        "news_count": News.objects.count()
    }