from django.contrib import admin
from news.models import News, Tag, Author
# Register your models here.

class NewsInline(admin.TabularInline):
    model = News
    extra = 0
    fields = ('title', 'content', 'pub_date')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "birth_date", "is_live"]
    inlines = [NewsInline]


    def is_live(self, obj):
        if obj.death_date:
            return False
        return True

    is_live.boolean = True