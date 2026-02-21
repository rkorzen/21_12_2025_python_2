import pytest
from django.urls import reverse

from blog.factories import PostFactory


@pytest.mark.django_db
def test_detail_page_contains_post_title(client, post):
    response = client.get(reverse("blog:details", args=[post.id]))

    assert response.status_code == 200
    assert post.title in response.content.decode()

@pytest.mark.django_db
def test_list_page_contains_post_titles(client):
    posts = PostFactory.create_batch(3)
    response = client.get(reverse("blog:list"))

    for post in posts:
        assert post.title in response.content.decode()

    assert len(posts) == response.context["page_obj"].paginator.count


