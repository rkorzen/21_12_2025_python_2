
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    def length(self):
        return len(self.content)

    def get_snippet(self):
        return self.content[:100] + "..."

