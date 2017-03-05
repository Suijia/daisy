# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers.BaseHandler import BaseHandler
import utils.EmailFeedback as Email

__author__ = 'pudding'


class FeedbackHandler(BaseHandler):
    def initialize(self, conf):
        super(FeedbackHandler, self).initialize(conf)

    def get(self):
        self.render_with_user('feedback.html')

    def post(self):
        title = self.get_argument("title", "")
        content = self.get_argument("content", "")
        email = self.get_argument("email", "")
        tornado.log.app_log.info("receive feedback:\n title: {0}\ncontent: {1}\nemail: {2}".format(
            title.encode('utf-8'), content.encode('utf-8'), email.encode('utf-8')))

        if title == "":
            self.write("写个标题吧")
            return

        if len(content) < 10:
            self.write("多写几句吧TT")
            return

        if email == "":
            self.write("请填写正确的邮箱")
            return

        password = self.conf.get('email_password', "")

        title = u"【用户反馈】" + title
        content = \
            "==========================================\n" \
            "{0}\n" \
            "------\n" \
            "Email: {1}\n" \
            "==========================================\n".format(
                content.encode('utf-8'), email.encode('utf-8')).decode("utf-8")
        Email.send_mail_feedback(title, content, password)

        self.write("SUCC")
