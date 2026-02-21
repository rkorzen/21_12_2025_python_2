from .services import blog

def posts_count(request):
    return {'posts_count': blog.count_posts()}