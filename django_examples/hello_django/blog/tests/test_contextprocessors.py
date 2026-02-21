import pytest

from blog.factories import PostFactory


@pytest.mark.django_db
def test_post_count(client):
    response = client.get("/")
    assert response.context["posts_count"] == 0

    PostFactory.create_batch(3)

    response = client.get("/")
    assert response.context["posts_count"] == 3