import os

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import FileForms
from .models import SsrModel, BlogPost, BlogTag, BlogCategory, BlogComment
from .utils import getSsrList
import uuid
import threading
import markdown


# Create your views here.

class IndexView(View):
    def get(self, request):
        # categoryList = BlogCategory.objects.values_list("id","name").order_by("-create_time").limit(5)
        # postList = BlogPost.objects.values_list("category__cate_name","tag__tag_name","name","author").order_by("-create_time").limit(5)
        categoryList = BlogCategory.objects.order_by("-create_time")[:5]
        postList = BlogPost.objects.order_by("-add_time")[:5]
        postHotList = BlogPost.objects.order_by("-click_nums")[:5]
        parms = dict(categoryList=categoryList, postList=postList,postHotList=postHotList)
        return render(request, "index.html", parms)


class CategoryView(View):
    def get(self, request, category_id):
        categoryList = BlogCategory.objects.all()
        category = BlogCategory.objects.filter(id=category_id).first()
        postList = BlogPost.objects.filter(category__id=category_id).all()
        for post in postList:
            post.content = markdown.markdown(post.content,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ], safe_mode=True, enable_attributes=False)
        parms = dict(category=category, categoryList=categoryList, postList=postList)
        return render(request, "post.html", parms)


class PostView(View):
    def get(self, request, post_id=None):
        categoryList = BlogCategory.objects.all()
        if post_id:
            post = BlogPost.objects.filter(id=post_id).first()
            post.click_nums+=1
            post.save()
            post.content = markdown.markdown(post.content,
                                             extensions=[
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.toc'
                                             ])
            parms = dict(post=post, categoryList=categoryList)
            return render(request, "postInfo.html", parms)
        else:
            dataDict = request.GET
            page = dataDict.get("page", 1)
            per_page = dataDict.get("per_page", 6)
            key_word = dataDict.get("key_word", None)
            if key_word:
                post_lists = BlogPost.objects.filter(
                    Q(name__contains=key_word) | Q(content__contains=key_word)).order_by(
                    "-add_time").all()
            else:
                post_lists = BlogPost.objects.order_by(
                    "-add_time").all()
            paginator = Paginator(post_lists, per_page)
            postList = paginator.get_page(page)
            for post in postList:
                post.content = markdown.markdown(post.content,
                                                 extensions=[
                                                     'markdown.extensions.extra',
                                                     'markdown.extensions.codehilite',
                                                     'markdown.extensions.toc',
                                                 ], safe_mode=True, enable_attributes=False)

            parms = dict(postList=postList, categoryList=categoryList)
            return render(request, "post.html", parms)


class CommentView(View):
    def get(self, request):
        pass

    def post(self, request):
        dataDict = request.POST
        nick_name = dataDict.get("nick_name", None)
        email = dataDict.get("email", None)
        content = dataDict.get("content", None)
        post_id = dataDict.get("post_id", None)
        if not (nick_name and email and content and post_id):
            return JsonResponse({"code": -1, "msg": "参数不足", "data": {}})
        post = BlogPost.objects.filter(id=post_id).first()
        try:
            comment = BlogComment(nick_name=nick_name, email=email, content=content, post=post)
            comment.save()
        except:
            return JsonResponse({"code": -1, "msg": "留言失败", "data": {}})
        return JsonResponse({"code": 0, "msg": "", "data": {}})


class SsrListView(View):
    def get(self, request):
        ssrlist = SsrModel.objects.all()
        return render(request, "ssrList.html", {"ssrList": ssrlist})

    def post(self, request):
        path = str(uuid.uuid4()).replace("-", "") + ".txt"
        # path = getSsrList(path)
        threading.Thread(target=getSsrList, args=(path,)).start()
        ssr = SsrModel()
        ssr.path = path
        ssr.save()
        return redirect(reverse("ssrList", args=[]))
        # return HttpResponseRedirect(reverse("ssrList"))


class DownLoadView(View):
    def get(self, request, path):
        BASE_DIR = settings.BASE_DIR
        basepath = os.path.join(os.path.join(BASE_DIR, "upload"), "ssr")
        filename = os.path.join(basepath, path)
        file = open(filename, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="ssr.txt"'
        return response

    def post(self, request):
        fileforms = FileForms(request.POST)
        if fileforms.is_valid():
            path = request.POST.get("path")
            BASE_DIR = settings.BASE_DIR
            basepath = os.path.join(os.path.join(BASE_DIR, "upload"), "ssr")
            path = os.path.join(basepath, path)
            try:
                file = open(path, 'rb')
                response = FileResponse(file)
                # response = StreamingHttpResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="ssr.txt"'
                return response
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse("ssrList"))
        else:
            return HttpResponseRedirect(reverse("ssrList"))
