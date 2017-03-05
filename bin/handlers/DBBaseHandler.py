#!/usr/bin/env python
# -*-coding:utf-8-*-

import torndb
from BaseHandler import BaseHandler
from utils.MysqlLogger import MysqlLogger

__author__ = 'pudding'


class DBBaseHandler(BaseHandler):
    def initialize(self, conf):
        super(DBBaseHandler, self).initialize(conf)
        self.db = torndb.Connection(
            host=str(self.conf['database']['host']) + ':' + str(self.conf['database']['port']),
            database=str(self.conf['database']['database']),
            user=str(self.conf['database']['username']),
            password=str(self.conf['database']['password']))
        MysqlLogger.logger.info("{0} {1}".format(self.db.host, self.db.database))
