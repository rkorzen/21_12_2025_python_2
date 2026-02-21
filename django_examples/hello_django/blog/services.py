from .models import Post
from .factories import PostFactory

class DjangoBlog:
    def __init__(self):
        self._posts = Post.objects

    @property
    def posts(self):
        return self._posts.all()

    def get_post(self, id: int) -> Post:
        return self._posts.get(id=id)

    def generate_n_fake_posts(self, n: int) -> list[Post]:
        return PostFactory.create_batch(n)

    def count_posts(self):
        return self._posts.count()


blog = DjangoBlog()