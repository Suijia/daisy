#!/usr/bin/env python
# -*-coding:utf-8-*-
import random
import time

from utils.CrawlerLogger import CrawlerLogger
from lxml import etree

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:28
# filename: util.py
# ==============================


def get_text(element, pattern, use_text):
    texts = element.xpath(pattern)
    if len(texts) == 0:
        CrawlerLogger.logger.info("get text error {0} {1}".format(etree.tostring(element), pattern))
        return ""
    if use_text:
        # print etree.tostring(texts[0])
        text = texts[0].text
    else:
        text = texts[0]
    # print text
    return text


def sleep_random(start, end, interval=1, added=""):
    seconds = random.randint(start, end)
    print_sleep(seconds, interval, added)


def print_sleep(second, interval=1, added=''):
    """
    允许添加一条附加消息
    """
    CrawlerLogger.logger.info('' + added + '[' + str(second) + '],')
    if interval < 1:
        interval = 1
    while second > 0:
        if second > interval:
            time.sleep(interval)
            second -= interval
        else:
            time.sleep(second)
            second -= second
        CrawlerLogger.logger.info('' + added + '[' + str(second) + '],')

if __name__ == '__main__':
    print_sleep(10, 1, "test")
