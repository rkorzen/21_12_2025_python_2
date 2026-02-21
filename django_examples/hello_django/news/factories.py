import factory
from uuid import uuid4
from django.contrib.auth import get_user_model

from .models import Tag, Author


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda _: f"tag_{uuid4().hex[:8]}")
    slug = factory.LazyAttribute(lambda _: f"tag-{uuid4().hex}")


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.Faker('date_of_birth')
    death_date = factory.Faker('date_between', start_date='-10y', end_date='now')
    created_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
            return
        self.tags.add(TagFactory())


"""

from news.factories import AuthorFactory
a = AuthorFactory()
"""