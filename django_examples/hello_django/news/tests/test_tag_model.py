import pytest

from news.models import Tag
from news.factories import TagFactory

@pytest.mark.django_db
def test_save_whem_slug_is_none():
    tag = Tag(name="test")
    assert not tag.slug
    tag.save()
    assert tag.slug == "test"