# Create your views here.
import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import filters
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework_extensions.mixins import CacheResponseMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from url_filter.integrations.drf import DjangoFilterBackend

from utils.persimissons import IsOwnerOrReadOnly
from .models import BlogPost, BlogCategory, BlogTag, BlogComment, BlogCollection
from .serializers import UserSerializer, PostSerializer, CategorySerializer, TagSerializer, CommentSerializer, \
    CollectionSerializer

User = get_user_model()


class GoodsPagination(PageNumberPagination):
    """
    定制分页 更加灵活 前端可以自定义分页大小
    """
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class CustomBackend(ModelBackend):
    """
    自定义用户验证 默认会被django调用 因为jwt也是用的django的用户验证
    在 settings 中 配置 AUTHENTICATION_BACKENDS
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticatedOrReadOnly()]  # 权限
        elif self.action == 'create':
            return []
        else:
            return []


# class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
class PostViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)  # 配置 throttle来限制用户访问次数
    queryset = BlogPost.objects.all().order_by('-add_time')
    serializer_class = PostSerializer
    pagination_class = GoodsPagination  # 使用自定义分页
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    # from .filters import  GoodsFilter
    # filter_class = GoodsFilter
    filter_fields = ['name', "content"]

    # filter_fields = ('category',)
    # search_fields = ("name", 'category__cate_name')  # 可搜索 字段
    # ordering_fields = ('click_nums', 'fav_nums')  # 可 使用排序字段

    # 重写RetrieveModelMixin 中的方法
    def retrieve(self, request, *args, **kwargs):
        print("inone")
        instance = self.get_object()  # get_objcet获取到serializer的实例
        instance.click_nums += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True)  # , renderer_classes=[renderers.StaticHTMLRenderer] 渲染格式  # renderers
    def highlight(self, request, *args, **kwargs):
        print("intwo")
        post = self.get_object()
        post.click_nums += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    # 不知道有什么用 获取实例
    # def get_object(self):
    #     return self.request.user


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.filter(category_type=1).order_by('-create_time')
    serializer_class = CategorySerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    # filter_class = GoodsFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = BlogTag.objects.all().order_by('-create_time')
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all().order_by('-create_time')

    # serializer_class = CommentSerializer # 通用 serializer 或者使用 get_serializer_class() 不同对应不同

    # 认证权限
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    @action(detail=True)
    def delete(self, request, *args, **kwargs):
        print("intwo")
        comment = self.get_object()
        comment.is_delete = 0
        comment.content = "内容已删除！！"
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = 0
        instance.content = "内容已删除！！"
        instance.save()
        # self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 启动验证
        email = serializer.validated_data['email']
        print(email)
        serializer.save()
        # self.perform_create(serializer) # 也可以不调用 直接  serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # 先调用 ViewSet 中的 viewset.create ---> perform_create (when serializer.save()) -->serializer.create
        # 同理 update 等操作 应该也一样
        print("one")
        shopcart = serializer.save()  # 获取购物车商品
        print("three")
        print(shopcart.email)

    # 不同请求 使用不同的serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CommentSerializer
        elif self.action == 'create':
            return CommentSerializer
        return CommentSerializer


class CollectionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.DestroyModelMixin):
    # queryset = BlogCollection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_queryset(self):
        print("in")
        return BlogCollection.objects.filter(user=self.request.user)

from django.views import View
from django.shortcuts import render
class SocialTemp(View):
    def get(self,request):
        return render(request,"index.html")
