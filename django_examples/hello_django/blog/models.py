
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def length(self):
        return len(self.content)

    @classmethod
    def fake(cls, id):
        return ...

    def get_snippet(self):
        return self.content[:100] + "..."

