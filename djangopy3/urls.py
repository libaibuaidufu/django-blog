"""djangopy3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import TemplateView
from django.views.static import serve

from djangopy3.settings import MEDIA_ROOT
from posts.views import PostsView,CategoryView,ArticleView,ReadersView,TagView,SearchView
from users.views import LoginView,LogoutView,RegisterView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$',RegisterView.as_view(),name='register'),

    url(r'^$',PostsView.as_view(),name='index'),
    url(r'^category/(?P<category_id>\d)$',CategoryView.as_view(),name='category'),
    url(r'^post/(?P<post_id>\d+)$',ArticleView.as_view(),name='article'),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^readers/$',ReadersView.as_view(),name='readers'),
    url(r'^tag/$',TagView.as_view(),name='tag'),
    #配置富文本
    url(r'^tinymce/', include('tinymce.urls')),
    # xadmin 集成富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # 配置上次文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
