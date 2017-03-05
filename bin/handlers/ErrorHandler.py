# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers.BaseHandler import BaseHandler

__author__ = 'pudding'


class ErrorHandler(BaseHandler):

    def initialize(self, conf):
        super(ErrorHandler, self).initialize(conf)

    def get(self):

        self.render_with_user('404.html')

    post = get
