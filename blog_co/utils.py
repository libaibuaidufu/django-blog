#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/5/29 16:30
@File    : utils.py
@author  : dfkai
@Software: PyCharm
"""
import logging
from hashlib import md5

import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name

logger = logging.getLogger(__name__)


def get_md5(str):
    m = md5(str.encode('utf-8'))
    return m.hexdigest()


def send_email(emailto, title, content):
    from blog_co.blog_signals import send_email_signal
    send_email_signal.send(
        send_email.__class__,
        emailto=emailto,
        title=title,
        content=content)


def block_code(text, lang, inlinestyles=False, linenos=False):
    '''
    markdown代码高亮
    :param text:
    :param lang:
    :param inlinestyles:
    :param linenos:
    :return:
    '''
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except BaseException:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'


class CommonMarkdown():
    @staticmethod
    def get_markdown(value):
        markdown = mistune.create_markdown(renderer=HighlightRenderer())
        return markdown(value)


