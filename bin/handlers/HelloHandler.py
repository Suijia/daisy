# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers.BaseHandler import BaseHandler

__author__ = 'pudding'


class HelloHandler(BaseHandler):
    def initialize(self, conf):
        super(HelloHandler, self).initialize(conf)

    def get(self):
        title_list = ["I am pudding", "I am snowwolf"]
        self.render_with_user('hello.html', title_list=title_list)

    post = get
