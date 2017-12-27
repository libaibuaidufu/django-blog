# coding:utf-8
__author__ = "dfk"
__date__ = "2017/12/24 12:01"

import xadmin
from xadmin import views

from .models import Tag, Post, Backimage,Comment


# 使用主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


# xamdin全局修改
class GlobalSettings(object):
    site_title = '随风潜入夜'
    site_footer = '个人博客'
    menu_style = 'accordion'


class Tagadmin(object):
    list_display = ['name', 'add_time']
    search_fields = []
    list_filter = ['name', 'add_time']


class PostAdmin(object):
    list_display = ['user', 'tag', 'name', 'content', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'content', 'fav_nums', 'click_nums']
    list_filter = ['user__username', 'tag', 'name', 'content', 'fav_nums', 'click_nums', 'add_time']
    style_fields = {"content": "ueditor"}

class CommentAdmin(object):
    list_display=['user','post','content','add_time']
    search_fields=['content']
    list_filter=['user__username','post__name','content','add_time']

class BackimageAdmin(object):
    list_display = ['name', 'image', 'add_time']
    search_fields = ['name', 'image']
    list_filter = ['name', 'image', 'add_time']


xadmin.site.register(Tag, Tagadmin)
xadmin.site.register(Post, PostAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Backimage, BackimageAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
