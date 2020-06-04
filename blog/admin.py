from django.contrib import admin

from .models import Article, Category, Tag


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", 'pub_time', 'status', 'comment_status', 'type', 'views', 'author', 'article_order',
                    'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category', 'slug']


class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagsAdmin)
