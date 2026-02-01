from dataclasses import dataclass
from faker import Faker

faker = Faker("pl_PL")

@dataclass
class Book:
    id: int
    title: str
    ...

    def fake(self):
        return Book(self.id, title=faker.text(max_nb_chars=80))

class DummyDb:
    def __init__(self):
        self.books = []

    def generate_n_fake_books(self, n: int):
        for i in range(n):
            self.books.append(Book(i, faker.text(max_nb_chars=80)))

    def all(self):
        return self.books

    def get(self, id):
        return next(filter(lambda book: book.id == id, self.books))


class BookService:

    def __init__(self, db: DummyDb):
        self.db = db

    def get_books(self):
        return self.db.all()

    def get_book(self, id):
        return self.db.get(id)

db = DummyDb()
db.generate_n_fake_books(100)

book_service = BookService(db)
