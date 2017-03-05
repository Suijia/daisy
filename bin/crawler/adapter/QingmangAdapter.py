#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import requests
from utils.CrawlerLogger import CrawlerLogger
from model import Doc
import time

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:19
# filename: QingmangAdapter.py
# ==============================


class QingmangAdapter:
    def __init__(self, seed_url='', source=u'微信公众号', channel=u"不存在"):
        self.seed_url = seed_url
        self.source = source
        self.channel = channel

    def get_docs(self):
        doc_list = list()
        content = self.get_list_content(self.seed_url)
        result = json.loads(content)

        if result.get('entity', None) and len(result.get('entity', [])) > 0:
            for entity in result.get('entity'):
                if entity.get('sub_entity', None) and len(entity.get('sub_entity', [])) > 0:
                    for sub_entity in entity.get('sub_entity', None):
                        title = sub_entity.get("title", "")
                        detail_url = sub_entity.get("action", dict()).get("url", "")
                        snippet = sub_entity.get("snippet", "")
                        covers = sub_entity.get("cover", [])
                        cover = ""
                        if len(covers) > 0:
                            cover = covers[0].get('url', "")

                        author = ""

                        published_time = sub_entity.get("datePublished", int(time.time()) * 1000) / 1000

                        doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)
                        CrawlerLogger.logger.info("get doc" + str(doc))
                        doc_list.append(doc)
        return doc_list

    def get_list_content(self, tmp_url):
        """
        获取详情页内容
        :param tmp_url: 带时间戳的临时url
        :return:
        """
        CrawlerLogger.logger.info("temp url: " + tmp_url)
        try:
            r = requests.get(tmp_url)
            if r.status_code == 200:
                return r.text
            else:
                CrawlerLogger.logger.warn("request tmp_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return ""
        except Exception as e:
            CrawlerLogger.logger.warn("request tmp_url error {0} {1}".format(self.seed_url, e))
            return ""


if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    # adapter = MediaPressAdapter(
    #     seed_url='http://weixin.sogou.com/weixin?type=1&query=non-exist-FAA')
    adapter = QingmangAdapter(
        seed_url='http://ripple.qingmang.me/api/v2/feed.json?providerId=7102&max=30', channel=u"不存在")
    adapter.get_docs()
    # ls = "http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==\x26amp;mid=2650721480\x26amp;idx=1\x26amp;sn=191cb46a8ebbb71519d5d668705aa81b\x26amp;chksm=871b08b6b06c81a0265fc5de459f78cd5e1e887f3569f57a2e7ccb4ff7835d73c66699cc483a#rd"
    # print ls.replace('\x26amp;', '&')


