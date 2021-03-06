"""blog_co URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url("", include("blog.urls")),
                  url("", include("users.urls")),
                  url(r'^search/', include('haystack.urls')),
                  # re_path('^stiaic/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}),  # 用于处理static里的文件
                  # re_path('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),  # 用于处理上传的文件
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# debug =False 时，静态文件主要靠配置
