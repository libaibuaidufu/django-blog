"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import xadmin
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from djangoblog.settings import MEDIA_ROOT
from users.views import IndexView,PostView,LoginView,CommentView,RegisterView,LogoutView,UserdetailView,ResetpwdView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^login/$', LoginView.as_view(), name='login'),

    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^user/$', UserdetailView.as_view(), name='user_datail'),

    url(r'^register/$', RegisterView.as_view(), name='register'),

    url(r'^resetpwd/$', ResetpwdView.as_view(), name='resetpwd'),

    url(r'^add_comment/$', CommentView.as_view(), name='add_comment'),

    url(r'^post/(?P<post_id>\d*)$',PostView.as_view(),name='post'),

    # 配置上次文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # xadmin 集成富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]
