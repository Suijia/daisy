# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
import base64
import json
from crawler.QuizDao import QuizDao
from handlers.BaseHandler import BaseHandler

__author__ = 'pudding'


class OpsHandler(BaseHandler):
    def initialize(self, conf):
        super(OpsHandler, self).initialize(conf)

    def get(self):

        self.render_with_user('ops.html')

    def post(self):
        file_obj = self.get_argument('file_obj', "")

        if len(file_obj) == 0:
            self.write(json.dumps({'ok': True, 'desc': "输入文件为空"}))
            return
        token = self.get_argument('token', "")
        if len(token) == 0:
            self.write(json.dumps({'ok': True, 'desc': "输入token为空"}))
            return

        if token != self.conf.get("ops_token", ""):
            self.write(json.dumps({'ok': True, 'desc': "输入token不正确"}))
            return

        file_obj_content = file_obj.split(',')[1].encode('utf-8')
        file_obj_decode = base64.b64decode(file_obj_content)

        quiz_dao = QuizDao()
        total, succ = quiz_dao.import_from_lines(file_obj_decode.split("\n"))

        desc = "总共添加{0}条, 成功{1}条".format(total, succ)
        self.write(json.dumps({'ok': True, 'desc': desc}))
