from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class News(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField(null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, related_name='news')

    def __str__(self):
        author_name = self.author.short_name if self.author else "anonimowy"
        return f"{self.title} ({author_name} - {self.pub_date.strftime('%Y-%m-%d %H:%M:%S')})"

class Author(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    death_date = models.DateField(null=True)

    @property
    def short_name(self):
        short_name = self.first_name[0] + self.last_name[0]
        return short_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

