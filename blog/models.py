from abc import abstractmethod

from django.conf import settings
from django.db import models
from django.urls import reverse
from mdeditor.fields import MDTextField
from uuslug import slugify


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # is_update_views = isinstance(
        #     self,
        #     Article) and 'update_fields' in kwargs and kwargs['update_fields'] == ['views']
        # if is_update_views:
        #     Article.objects.filter(pk=self.pk).update(views=self.views)
        # else:
        if 'slug' in self.__dict__:
            slug = getattr(
                self, 'title') if 'title' in self.__dict__ else getattr(
                self, 'name')
            setattr(self, 'slug', slugify(slug))
        super().save(*args, **kwargs)

    def get_full_url(self):
        # site = get_current_site().domain
        site = settings.SITE
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    @abstractmethod
    def get_absolute_url(self):
        pass


class Article(BaseModel):
    """文章"""
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = MDTextField('正文')
    pub_time = models.DateTimeField(
        '发布时间', blank=False, null=False, auto_now_add=True)
    status = models.CharField(
        '文章状态',
        max_length=1,
        choices=STATUS_CHOICES,
        default='p')
    comment_status = models.CharField(
        '评论状态',
        max_length=1,
        choices=COMMENT_STATUS,
        default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    article_order = models.IntegerField(
        '排序,数字越大越靠前', blank=False, null=False, default=0)
    category = models.ForeignKey(
        'Category',
        verbose_name='分类',
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def get_body(self):
        return f"{self.title} {self.author.username} {self.body}"

    def body_to_string(self):
        return self.body

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-article_order', '-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def viewed(self):
        self.views += 1
        self.save()

    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    def get_tags_str(self):
        tag_name = []
        print(self.tags)
        print(self.tags.name)
        if self.tags.name:
            for tag in self.tags.name:
                print(tag)
                tag_name.append(tag)
        return "，".join(tag_name)


class Category(BaseModel):
    """文章分类"""
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey(
        'self',
        verbose_name="父级分类",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:categorybyslug', kwargs={
            'category_name': self.slug
        })

    def get_category_tree(self):
        """
        递归获得分类目录的父级
        :return:
        """
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys

    def get_sub_categorys(self):
        """
        获得当前分类目录所有子集
        :return:
        """
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


class Tag(BaseModel):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:tagbyslug', kwargs={'tag_name': self.slug})


class Comment(models.Model):
    body = models.TextField('正文', max_length=300)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='作者',
        on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article,
        verbose_name='文章',
        on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self',
        verbose_name="上级评论",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)

    class Meta:
        ordering = ['id']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.body

    def get_sub_categorys(self):
        """
        获得当前分类目录所有子集
        :return:
        """
        comments = []
        all_comments = Comment.objects.all()

        def parse(comment):
            if comment not in comments:
                comments.append(comment)
            childs = all_comments.filter(parent_comment=comment)
            for child in childs:
                if comment not in comments:
                    comments.append(child)
                parse(child)

        parse(self)
        return comments
