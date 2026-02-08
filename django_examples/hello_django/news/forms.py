from django import forms
from .models import News, Author

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        exclude = ('tags',)

class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        exclude = ('tags',)


"""
author_data = {
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "1970-01-01",
}

form = AuthorForm(data=author_data)
if form.is_valid():
    a = form.save()


news_data = {
 'title': 'aaa',
 'content': 'cos tam',
 'pub_date': '2026-02-08 17:12',
 'author': 3
 }
"""