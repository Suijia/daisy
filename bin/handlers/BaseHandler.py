#!/usr/bin/env python
# -*-coding:utf-8-*-

import tornado.web
import tornado.log

__author__ = 'pudding'


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, conf):
        self.conf = conf
        tornado.log.app_log.info(
            "get request: [" + self.request.host + '][' + self.request.method + ']' + self.request.path)

    def render_with_user(self, template_name, **kwargs):
        user = self.get_current_user()

        if "localhost" not in self.request.host and "120.27.111.29" not in self.request.host \
                and "127.0.0.1" not in self.request.host \
                and "100.64.84.146" not in self.request.host \
                and "pudding.space" not in self.request.host:
            self.render('404.html')
            return

        if user is None:
            self.redirect(self.get_login_url())
        else:
            kwargs['user'] = user
            self.render(template_name, **kwargs)

    def get_login_url(self):
        return '/login'

    def get_current_user(self):
        return "NULL"

    def get_logout_url(self):
        self.clear_cookie('user_token')
        return self.get_login_url()

    def write_error(self, status_code, **kwargs):
        print 'In get_error_html. status_code: ', status_code
        exc_info = kwargs.get('exc_info', None)
        err_str = str(exc_info)
        if status_code in [403, 404, 500, 503]:
            self.render_with_user('500.html', status_code=status_code, err_str=err_str)
        else:
            self.write('BOOM!')

    def render_403(self):
        self.render_with_user('403.html')
