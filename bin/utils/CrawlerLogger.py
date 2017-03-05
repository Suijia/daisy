# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging.handlers


class CrawlerLogger(object):
    """ 单独保存 log 中关于 crawler 的操作记录 """
    logger = logging.getLogger("handlers.crawler.log")

    @staticmethod
    def set_up(log_file):
        formatter = logging.Formatter(
            "[%(levelname)1.1s %(asctime)s %(process)d:%(thread)d %(module)s:%(lineno)d] %(message)s")
        file_handler_mysql = logging.handlers.WatchedFileHandler(log_file)
        file_handler_mysql.setFormatter(formatter)
        CrawlerLogger.logger.addHandler(file_handler_mysql)
        CrawlerLogger.logger.setLevel(logging.INFO)
