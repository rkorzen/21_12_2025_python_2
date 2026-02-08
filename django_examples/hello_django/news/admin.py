from django.contrib import admin
from news.models import News, Tag, Author

from django.db.models import Case, When, Value, IntegerField, Count
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
    list_display = ["first_name", "last_name", "birth_date", "is_live", "news_count"]
    inlines = [NewsInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            is_live_order=Case(
                When(death_date__isnull=False, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            ),
            news_total=Count("news")
        )

    def is_live(self, obj):
        if obj.death_date:
            return False
        return True

    is_live.boolean = True
    is_live.short_description = "Żyje"
    is_live.admin_order_field = "is_live_order"


    def news_count(self, obj):
        return obj.news_total

    news_count.admin_order_field = "news_total"
    news_count.short_description = "Liczba newsów"
