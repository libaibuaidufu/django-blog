from django.contrib import admin

from .models import Post, Category,Tell,TodayOne,Comment,Tag


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user']

class PostAdmin(admin.ModelAdmin):
    list_display = ['name']

class TellAdmin(admin.ModelAdmin):
    list_display = ['name']

class TodayOneAdmin(admin.ModelAdmin):
    list_display = ['name']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tell, TellAdmin)
admin.site.register(TodayOne, TodayOneAdmin)
admin.site.register(Tag, TagAdmin)
