import pytest
from blog.factories import PostFactory


# Create your tests here.
class PostModelTest:

    @pytest.mark.parametrize(
        "content,length",
        [
            ("ABC", 3),
            ("ABC123", 6),
            ("A  B C 1 2  3", 13),
            ("   A  B C 1 2  3    ", 20),
        ]
    )
    def test_length_method(self, content, length):
        p = PostFactory.build(content=content)
        assert p.length() == length

    def test_get_snippet_for_short_content(self, post_with_short_content):
        assert post_with_short_content.get_snippet() == "ABC..."

    def test_get_snippet_for_long_content(self, post_with_long_content):
        assert post_with_long_content.get_snippet() == "a"*100 + "..."

