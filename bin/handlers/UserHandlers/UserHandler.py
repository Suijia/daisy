#!/usr/bin/env python
# -*-coding: utf-8-*-
from handlers.DBBaseHandler import DBBaseHandler
import tornado.log
__author__ = 'pudding'


# ==============================
# author: pudding
# created at: 16/8/2 下午9:52
# filename: UserHandler.py
# ==============================

class UserHandler(DBBaseHandler):
    def initialize(self, conf):
        super(UserHandler, self).initialize(conf)
        tornado.log.app_log.info("UserHandler begin")


    def get(self):
        users = self.get_all_user()
        tornado.log.app_log.info("UserHandler size: {0}".format(len(users)))

    def get_all_user(self):
        sql = 'select * from user'
        users = self.db.query(sql)
        return users
