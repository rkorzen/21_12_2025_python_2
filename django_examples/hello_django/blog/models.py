from django.db import models
from dataclasses import dataclass

@dataclass
class Post:
    id: int
    title: str
    content: str

    def length(self):
        return len(self.content)
# Create your models here.
class Blog:

    def __init__(self):
        self.posts: list[Post] = []

    def get_post(self, id: int) -> Post:
        return next(filter(lambda post: post.id == id, self.posts))


blog = Blog()
blog.posts.append(Post(1, "Hello World", "This is my first blog post!"))
blog.posts.append(Post(2, "Hello Django", "This is my second blog post!"))



