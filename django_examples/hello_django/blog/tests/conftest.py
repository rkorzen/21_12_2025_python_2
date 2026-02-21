import pytest
from blog.factories import PostFactory

@pytest.fixture
def post():
    return PostFactory()


@pytest.fixture
def post_with_short_content():
    return PostFactory.build(content="ABC")


@pytest.fixture
def post_with_long_content():
    t = ""
    for i in range(200):
        t += "a"

    return PostFactory.build(content=t)
