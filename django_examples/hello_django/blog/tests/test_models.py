
from blog.factories import PostFactory

# Create your tests here.
class PostModelTest:

    def test_length_method(self):
        p = PostFactory.build(content = "ABC")
        assert p.length() == 3

        p = PostFactory.build(content = "ABC123")
        assert p.length() == 6

        p = PostFactory.build(content="A  B C 1 2  3")
        assert p.length() == 6 + 7

        p = PostFactory.build(content="   A  B C 1 2  3    ")
        assert p.length() == 6 + 7