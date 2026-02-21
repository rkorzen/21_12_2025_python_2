import factory
from .models import Book

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker('sentence')
    author = factory.Faker('name')
    published_year = factory.Faker('year')
    is_avilable = factory.Faker('boolean')