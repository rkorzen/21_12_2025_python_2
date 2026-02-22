from django.db import models
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES =  sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        max_length=100,
        default="python",
        choices=LANGUAGE_CHOICES
    )
    style = models.CharField(
        max_length=100,
        choices=STYLE_CHOICES,
        default="friendly"
    )

    owner = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="snippets")
    highlighted = models.TextField()

    class Meta:
        ordering = ["created"]


    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)

        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)