from django.db import models
from dataclasses import dataclass
from faker import Faker

faker = Faker("pl_PL")


@dataclass
class Post:
    id: int
    title: str
    content: str

    def length(self):
        return len(self.content)

    @classmethod
    def fake(cls, id):
        return cls(id, faker.text(max_nb_chars=80), faker.paragraph(50))

    def get_snippet(self):
        return self.content[:100] + "..."

# Create your models here.
class Blog:

    def __init__(self):
        self.posts: list[Post] = []

    def get_post(self, id: int) -> Post:
        return next(filter(lambda post: post.id == id, self.posts))


    def generate_n_fake_posts(self, n: int) -> list[Post]:
        for i in range(n):
            id = self.posts[-1].id + 1 if self.posts else 1
            self.posts.append(Post.fake(id))

    def count_posts(self):
        return len(self.posts)

class DjangoBlog:
    def __init__(self):
        ...

    def get_post(self, id: int) -> Post:
        ...

    def generate_n_fake_posts(self, n: int) -> list[Post]:
        ...

    def count_posts(self):
        ...


blog = DjangoBlog()
# blog.generate_n_fake_posts(500) # zrob to z reki 1 raz i zakomentuj



