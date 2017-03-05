# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging.handlers


class MysqlLogger(object):
    """ 单独保存 tags 中关于 mysql 的操作记录 """
    logger = logging.getLogger("handlers.mysql.log")

    @staticmethod
    def set_up(log_file):
        formatter = logging.Formatter("[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s")
        file_handler_mysql = logging.handlers.WatchedFileHandler(log_file)
        file_handler_mysql.setFormatter(formatter)
        MysqlLogger.logger.addHandler(file_handler_mysql)
        MysqlLogger.logger.setLevel(logging.INFO)
