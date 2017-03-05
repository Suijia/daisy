#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'pudding'

import tornado.web
import tornado.log

from BaseHandler import BaseHandler


class ConfigHandler(BaseHandler):
    def initialize(self, conf):
        super(ConfigHandler, self).initialize(conf)

    @tornado.web.authenticated
    def get(self):
        self.render("Config.html", user=self.get_current_user())

    post = get
