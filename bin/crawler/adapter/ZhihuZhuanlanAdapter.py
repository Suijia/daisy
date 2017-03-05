#!/usr/bin/env python
# -*-coding:utf-8-*-
import re
import requests
import time
from utils.CrawlerLogger import CrawlerLogger
from model import Doc
import json

__author__ = 'pudding'

# ==============================
# author: pudding
# created at: 16/8/7 下午9:44
# filename: ZhihuZhuanlanAdapter.py
# ==============================


class ZhihuZhuanlanAdapter:
    def __init__(self, seed_url='', source=u'知乎专栏', channel=u"星海航纪"):
        self.seed_url = seed_url
        self.source = source
        self.channel = channel

    def get_docs(self):
        doc_list = list()
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            r = requests.get(self.seed_url, verify=False, headers=headers)
            if r.status_code == 200:
                html_text = r.text
                # print html_text
            else:
                CrawlerLogger.logger.info("request seed_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return doc_list
        except Exception as e:
            CrawlerLogger.logger.info("request seed_url error {0} {1}".format(self.seed_url, e))
            return doc_list

        results = json.loads(html_text)
        index = 0
        for item in results:
            CrawlerLogger.logger.info('--------------------' + str(index))
            index += 1

            title = item.get('title', "")
            detail_url = "https://zhuanlan.zhihu.com" + item.get('url', "")
            snippet = item.get('content', "")
            dr = re.compile(r'<[^>]+>', re.S)  # 去除html标签
            snippet = dr.sub('', snippet)[0: min(200, len(snippet))]
            cover = item.get('titleImage', "")
            author = item.get('author', dict()).get("name", "")
            published_str = item.get('publishedTime', "")
            try:  # 2016-05-22T21:09:03+08:00
                published_str = published_str.split('+')[0]
                published_time = int(time.mktime(time.strptime(published_str, "%Y-%m-%dT%H:%M:%S")))
            except Exception as e:
                published_time = time.time()
                CrawlerLogger.logger.info("get publish time error {0}, {1}".format(published_str, e))

            doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)
            CrawlerLogger.logger.info("get doc" + str(doc))
            doc_list.append(doc)
        return doc_list


if __name__ == '__main__':
    adapter = ZhihuZhuanlanAdapter(seed_url='https://zhuanlan.zhihu.com/api/columns/interimm/posts?limit=20')
    adapter.get_docs()
