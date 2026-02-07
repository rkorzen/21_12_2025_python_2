from datetime import datetime
from typing import Protocol
from dataclasses import dataclass

@dataclass
class News:
    id: int
    title: str
    content: str
    is_published: bool
    date_of_publication: datetime

class NewsService(Protocol):

    def get_news(self) -> list[News]:
        """Returns all news"""
        ...

    def get_published_news(self) -> list[News]:
        ...

    def get_by_id(self, id) -> News:
        ...



class DummyNewsService:

    def __init__(self, db: list[News]):
        self.db = db

    def get_news(self):
        return self.db

    def get_published_news(self):
        return [n for n in self.db if n.is_published]

    def get_by_id(self, id) -> News:
        news = next(filter(lambda n: n.id == id, self.db), None)
        if not news:
            raise ValueError(f"No news with id {id}")
        return news


db = [
    News(1, "First", "Lorem ipsum", True, datetime.now()),
    News(2, "Second", "Lorem ipsum", False, datetime.now())
]

service = DummyNewsService(db)

if __name__ == "__main__":
    service = DummyNewsService(db)
    assert service.get_news() == db
    assert service.get_published_news() == [db[0]]
    assert service.get_by_id(2) == db[1]
