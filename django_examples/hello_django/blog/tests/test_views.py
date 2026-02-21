import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_detail_page_contains_post_title(client, post):
    response = client.get(reverse("blog:details", args=[post.id]))

    assert response.status_code == 200
    assert post.title in response.content.decode()