# blog-co
本文 学习、借鉴了 [DjangoBlog](https://github.com/liangliangyy/DjangoBlog).

## 主要区别
使用bootstrap4 写的前端样式
后端基本一致，没有那么复杂，例如缓存 压缩等功能都没有加入。
采用 django-elasticsarch-dsl 实现es搜索

## 配置
```
pip  install -r requirements.txt

配置 email
# 数据库生成
python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic

```
**注意**
页面模板 使用了cdn ，避免带宽小的服务器请求页面卡，因此用cdn，可以大大加速页面。
如果你的带宽比较大，可以在templates中 修改base.html 和 users/users_form_base.html
其中 tempmodel中的页面本来是准备做前后端分离的 后台发现不适合就弃用了

如果样式不对，可以设置debug=False

es 生成索引 `python manage.py search_index`

haystack 生成索引 `python manage.py rebuild_index`

### 使用中的 问题
```python
    from django.utils.encoding import force_text, python_2_unicode_compatible
ImportError: cannot import name 'python_2_unicode_compatible' from 'django.utils.encoding' (C:\Envs\blog_co\lib\site-packages\django\utils\encoding.py)

# 首先
pip install six
# 在你自己的虚拟环境下 site-packages有six.py 的目录下
cp six.py django.utils

# 修改 site-packages\haystack\inputs.py
from django.utils.encoding import force_text, python_2_unicode_compatible
# 改为
from django.utils.encoding import force_text
from six import python_2_unicode_compatible

```

加入了 django-suit==2.0a1 美化后台页面，但是此版本尚未发布，因此安装
`pip install https://github.com/darklow/django-suit/tarball/v2`

### 预览
 ![image](https://github.com/libaibuaidufu/django-blog/blob/master/preview_one.png)
 ![image](https://github.com/libaibuaidufu/django-blog/blob/master/preview_two.png)