"""django_blog_drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from rest_framework import routers
from rest_framework.authtoken import views as auth_view
from rest_framework.documentation import include_docs_urls

from django_blog_drf.settings import MEIDA_ROOT
from home import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'categorys', views.CategoryViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'collections', views.CollectionViewSet, base_name='collection')  # self.get_queryset()
urlpatterns = [
    # path('', include(router.urls)),  # 版本划分
    path('api/v1/', include(router.urls)),  # 版本划分
    path('admin/', admin.site.urls),
    # media相关配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEIDA_ROOT}),
    # drf 自动生成文档  需要安装一些 coreapi 之类的
    url(r'^docs/', include_docs_urls(title="????")),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', auth_view.obtain_auth_token),
    url('', include('social_django.urls', namespace='social')),
    path(r'index/', views.SocialTemp.as_view(), name="index"),  # 测试微博登录
]

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# 认证
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
