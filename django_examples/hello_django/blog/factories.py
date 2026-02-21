import factory
from .models import Post


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:

        model = Post

    title = factory.Faker('sentence')
    content = factory.Faker('paragraph')
    is_published = factory.Faker('boolean')