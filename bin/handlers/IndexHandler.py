# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers import BaseHandler
from crawler.DocDao import DocDao
import json

__author__ = 'pudding'


class IndexHandler(BaseHandler):

    def initialize(self, conf):
        super(IndexHandler, self).initialize(conf)

    def get(self):
        source = self.get_argument("source", None)
        channel = self.get_argument('channel', None)
        page = int(self.get_argument('page', 1))
        page_size = int(self.get_argument('max', 6))
        doc_dao = DocDao()
        docs = doc_dao.get_docs(source, channel, (page - 1) * page_size, page_size)

        if docs >= page_size:
            next_url = "page={0}&max={1}".format(page + 1, page_size)
        else:
            next_url = ""

        if page > 0:
            pre_url = "page={0}&max={1}".format(max(0, page - 1), page_size)
        else:
            pre_url = ""

        if source:
            pre_url = "{0}&source={1}".format(pre_url, source.encode('utf-8')) if len(pre_url) > 0 else ""
            next_url = "{0}&source={1}".format(next_url, source.encode('utf-8')) if len(next_url) > 0 else ""

        if channel:
            pre_url = "{0}&channel={1}".format(pre_url, channel.encode('utf-8')) if len(pre_url) > 0 else ""
            next_url = "{0}&channel={1}".format(next_url, channel.encode('utf-8')) if len(next_url) > 0 else ""

        current_url = "page={0}&max={1}".format(page, page_size)

        cover_list = []
        for doc in docs:
            cover_list.append(str(doc.docid)+"COVER_FLAG"+doc.cover)

        cover_str = "DOC_FLAG".join(cover_list)
        print cover_str

        self.render_with_user('index.html', docs=docs, current_url=current_url, next_url=next_url, pre_url=pre_url,
                              cover_str=cover_str)

    post = get
