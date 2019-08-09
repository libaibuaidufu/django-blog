from django.shortcuts import render
from django.views import View
# from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Post, Category, Comment, Tell, TodayOne, IndexAD, Tag
from users.models import UserProfile


# Create your views here.

class PostsView(View):
    """
    测试一下是否可行
    """

    def get(self, request):
        all_posts = Post.objects.all()

        hot_posts = Post.objects.filter(is_hot=True)[:5]

        all_category = Category.objects.all()

        all_tells = Tell.objects.all()[:5]

        todayone = TodayOne.objects.order_by('-add_time')[:1]

        keyword = request.GET.get('keyword', '')
        if keyword:
            all_posts = all_posts.filter(Q(name__icontains=keyword) | Q(content__icontains=keyword))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_posts, 5, request=request)

        all_posts = p.page(page)

        return render(request, 'index2.html', {
            'all_posts': all_posts,
            'all_category': all_category,
            'hot_posts': hot_posts,
            'all_tells': all_tells,
            'todayone': todayone,
        })


class CategoryView(View):
    def get(self, request, category_id):
        all_posts = Post.objects.filter(category__id=category_id).order_by('-add_time')
        category = Category.objects.get(id=category_id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_posts, 1, request=request)

        all_posts = p.page(page)

        return render(request, 'category.html', {
            'all_posts': all_posts,
            'category': category,
        })


class ArticleView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        all_comments = Comment.objects.filter(post__id=post_id)
        all_tags = post.tag.all()

        all_tags_id = [tag.id for tag in all_tags]
        tag_post = Post.objects.filter(tag__id__in=all_tags_id)

        post.click_nums += 1
        post.save()

        return render(request, 'article.html', {
            'post': post,
            'all_comments': all_comments,
            'all_tags': all_tags,
            'tag_post': tag_post

        })


class ReadersView(View):
    def get(self, request):
        all_user = UserProfile.objects.order_by('-comment_nums')[:4]

        return render(request, 'readers.html', {
            'all_user': all_user,
        })


class TagView(View):
    def get(self, request):
        all_tags = Tag.objects.order_by('tag_nums')[:20]

        return render(request, 'tags.html', {
            'all_tags': all_tags
        })


class SearchView(View):
    def get(self, request):
        all_posts = []
        keyword = request.GET.get('keyword', "")
        if keyword:
            all_posts = Post.objects.filter(Q(name__icontains=keyword) | Q(content__icontains=keyword))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

            # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_posts, 1, request=request)

        all_posts = p.page(page)

        return render(request, 'search.html', {
            'all_posts': all_posts,
        })
