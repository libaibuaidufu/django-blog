#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/28 16:21
@File    : urls.py
@author  : dfkai
@Software: PyCharm
"""
from django.urls import path

from .views import ArticleIndexView, ArticleDetailView, CategoryArticleView, TagArticleView, CommentPostView, \
    AuthorDetailView, ESSearchView

app_name = "blog"
urlpatterns = [
    path(r'', ArticleIndexView.as_view(), name="index"),
    path(r'article/<int:year>/<int:month>/<int:day>/<int:article_id>.html', ArticleDetailView.as_view(),
         name="detailbyid"),
    path(r'category/<slug:category_name>.html', CategoryArticleView.as_view(), name="categorybyslug"),
    path(r'tag/<slug:tag_name>.html', TagArticleView.as_view(), name="tagbyslug"),
    path('article/<int:article_id>/postcomment', CommentPostView.as_view(), name='postcomment'),
    path(r'author/<author_name>.html', AuthorDetailView.as_view(), name='author_detail'),
    path(r'author/<author_name>/<int:page>.html', AuthorDetailView.as_view(), name='author_detail_page'),
    path(r'es_search/', ESSearchView.as_view(), name='es_search'),
]
