from django import forms
from django.contrib.auth.views import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .documents import ArticleDocument
from .forms import CommentForm
from .models import Article, Category, Tag, Comment


# Create your views here.
class ArticleListView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = "index.html"
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article_list'
    paginate_by = 5
    page_kwarg = 'page'

    # 自定义
    # 页面类型，分类目录或标签列表等
    page_type = ""
    tag_name = ""

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(
            page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page


class ArticleIndexView(ArticleListView):
    queryset = Article.objects.filter(status='p')
    template_name = "index.html"
    context_object_name = "article_list"
    paginate_by = 5
    page_kwarg = 'page'

    # 自定义
    page_type = ""
    tag_name = ""


class ArticleDetailView(DetailView):
    context_object_name = "article"
    template_name = "article_detail.html"
    pk_url_kwarg = "article_id"
    model = Article

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.viewed()  # 增加一次点击
        self.obj = obj
        return obj

    def get_context_data(self, **kwargs):
        category_list = self.obj.category.get_category_tree()
        comment_form = CommentForm()
        user = self.request.user
        # 如果用户已经登录，则隐藏邮件和用户名输入框
        if user.is_authenticated and not user.is_anonymous and user.email and user.username:
            comment_form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            comment_form.fields["email"].initial = user.email
            comment_form.fields["name"].initial = user.username

        article_comments = self.obj.comment_set.all()
        kwargs['form'] = comment_form
        kwargs["category_list"] = category_list[::-1]
        kwargs["article_comments"] = article_comments
        kwargs["comment_count"] = len(article_comments) if article_comments else 0
        return super().get_context_data(**kwargs)


class CategoryArticleView(ListView):
    template_name = "index.html"
    context_object_name = "article_list"
    paginate_by = 5

    page_type = "分类目录归档"

    def get_queryset(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)
        self.category_name = category.name
        categorynames = list(
            map(lambda c: c.name, category.get_sub_categorys()))
        article_list = Article.objects.filter(
            category__name__in=categorynames, status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs["page_type"] = self.page_type
        kwargs["tag_name"] = self.category_name
        return super().get_context_data(**kwargs)


class TagArticleView(ListView):
    template_name = "index.html"
    context_object_name = "article_list"
    paginate_by = 5

    page_type = "分类目录归档"

    def get_queryset(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        self.tag_name = tag.name

        article_list = Article.objects.filter(
            tags__name=tag.name, status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs["page_type"] = self.page_type
        kwargs["tag_name"] = self.tag_name
        return super().get_context_data(**kwargs)


class CommentPostView(FormView):
    form_class = CommentForm
    template_name = 'article_detail.html'

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']

        article = Article.objects.get(pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        u = self.request.user

        if self.request.user.is_authenticated:
            print("In")
            form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            user = self.request.user
            form.fields["email"].initial = user.email
            form.fields["name"].initial = user.username

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user

        article_id = self.kwargs['article_id']
        article = Article.objects.get(pk=article_id)
        if not self.request.user.is_authenticated:
            email = form.cleaned_data['email']
            username = form.cleaned_data['name']

            user = get_user_model().objects.get_or_create(
                username=username, email=email)[0]
            # auth.login(self.request, user)
        comment = form.save(False)
        comment.article = article

        comment.author = user

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(
                pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment

        comment.save(True)
        return HttpResponseRedirect(
            "%s#div-comment-%d" %
            (article.get_absolute_url(), comment.pk))


class AuthorDetailView(ListView):
    template_name = "index.html"
    context_object_name = "article_list"
    paginate_by = 5

    page_type = "作者文章归档"

    def get_queryset(self):
        self.author_name = self.kwargs['author_name']
        article_list = Article.objects.filter(
            author__username=self.author_name, type='a', status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs["page_type"] = self.page_type
        kwargs["tag_name"] = self.author_name
        return super().get_context_data(**kwargs)


class ESSearchView(ListView):
    template_name = "search/es_search.html"
    context_object_name = "article_list"
    paginate_by = 5
    page_kwarg = "page"

    page_type = "搜索"
    tag_name = ""

    def get_queryset(self):
        query = self.request.GET.get('q')
        self.tag_name = query
        sqs_app = ArticleDocument.search().query("multi_match", query=query, fields=["body"])
        qs = sqs_app.to_queryset()
        return qs

    def get_context_data(self, **kwargs):
        kwargs["tag_name"] = self.tag_name
        kwargs["page_type"] = self.page_type
        return super().get_context_data(**kwargs)
