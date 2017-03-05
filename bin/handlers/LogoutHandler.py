#!/usr/bin/env python
#-*-coding:utf-8-*-
__author__ = 'pudding'

import tornado.web
import tornado.log

from BaseHandler import BaseHandler


class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.redirect(self.get_logout_url())
