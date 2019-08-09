#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 19:54
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
import base64
import urllib.request
import os
import uuid


def getSsrList(path):
    req = urllib.request.Request(url="https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com")
    rep = urllib.request.urlopen(req)
    data = rep.read()
    ssr_list = str(base64.urlsafe_b64decode(data), encoding="utf8").split("\n")
    basedir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), "upload"), "ssr")
    pathname = os.path.join(basedir, path)
    with open(pathname, "w+", encoding="utf8") as f:
        for ssr in ssr_list:
            f.write(ssr)
    return pathname, path


def getSsrFile():
    req = urllib.request.Request(url="https://raw.githubusercontent.com/AmazingDM/sub/master/ssrshare.com")
    rep = urllib.request.urlopen(req)
    data = rep.read()
    ssr_list = str(base64.urlsafe_b64decode(data), encoding="utf8").split("\n")
    path = str(uuid.uuid4()).replace("-", "")
    with open(path, "w+", encoding="utf8") as f:
        for ssr in ssr_list:
            f.write(ssr)
    return path


if __name__ == '__main__':
    path = str(uuid.uuid4()).replace("-", "")
    print(getSsrFile())
