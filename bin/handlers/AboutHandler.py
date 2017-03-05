# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers.BaseHandler import BaseHandler

__author__ = 'pudding'


class AboutHandler(BaseHandler):
    def initialize(self, conf):
        super(AboutHandler, self).initialize(conf)

    def get(self):
        self.render_with_user('about.html')

    post = get
