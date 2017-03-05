# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers.BaseHandler import BaseHandler
from crawler.DocDao import DocDao

__author__ = 'pudding'


class TestHandler(BaseHandler):

    def initialize(self, conf):
        super(TestHandler, self).initialize(conf)

    def get(self):
        source = self.get_argument("source", None)
        channel = self.get_argument('channel', None)
        start = int(self.get_argument('start', 0))
        page_size = int(self.get_argument('max', 10))
        doc_dao = DocDao()
        docs = doc_dao.get_docs(source, channel, start, page_size)

        if docs >= page_size:
            next_url = "start={0}&max={1}".format(start + page_size, page_size)
        else:
            next_url = ""

        if start > 0:
            pre_url = "start={0}&max={1}".format(max(0, start - page_size), page_size)
        else:
            pre_url = ""

        if source:
            pre_url = "{0}&source={1}".format(pre_url, source.encode('utf-8')) if len(pre_url) > 0 else ""
            next_url = "{0}&source={1}".format(next_url, source.encode('utf-8')) if len(next_url) > 0 else ""

        if channel:
            pre_url = "{0}&channel={1}".format(pre_url, channel.encode('utf-8')) if len(pre_url) > 0 else ""
            next_url = "{0}&channel={1}".format(next_url, channel.encode('utf-8')) if len(next_url) > 0 else ""

        current_url = "start={0}&max={1}".format(start, page_size)

        self.render_with_user('test.html', docs=docs, current_url=current_url, next_url=next_url, pre_url=pre_url)

    post = get
