#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import requests
from lxml import etree
from utils.CrawlerLogger import CrawlerLogger
import crawler.util as util
from model import Doc
import time
import re

__author__ = 'yangxj'

# ==============================
# author: yangxj
# created at: 16/8/7 上午9:19
# filename: NonExistAdapter.py
# ==============================


class NonExistAdapter:
    def __init__(self, seed_url='', source=u'微信公众号', channel=u"不存在"):
        self.seed_url = seed_url
        self.source = source
        self.channel = channel

    def get_docs(self):
        doc_list = list()
        # state_debug = 1
        catalog_html_text = self.get_query_content(self.seed_url)
        if catalog_html_text == "":
            CrawlerLogger.logger.error("get catalog html content error: {0}".format(self.seed_url.encode('utf-8')))
            return doc_list
        # fp = open('bin/crawler/adapter/list.html', 'w+')
        # old_pos = fp.tell()
        # fp.write(catalog_html_text.encode("utf-8"))
        # fp.seek(old_pos)  # seek 的作用?
        # catalog_html_text = fp.read()  # 读进来会变成 unicode
        # fp.close()
        list_url = NonExistAdapter.get_list_url(catalog_html_text)  # 获取各篇文章链接
        # print type(list_url)
        for detail_url in list_url:
            doc_content = self.get_query_content(detail_url)
            if doc_content == "":
                CrawlerLogger.logger.error("get one doc html content error: {0}".format(detail_url.encode('utf-8')))
                return doc_list
            doc = self.get_doc_from_content(doc_content, detail_url)
            doc_list.append(doc)
        print str(len(doc_list)) + ' docs have been found'
        return doc_list

    def get_query_content(self, real_url):
        """
        获取详情页内容
        :param real_url: 目录文章的url
        :return:
        """
        CrawlerLogger.logger.info("catalog url: " + real_url)
        try:
            r = requests.get(real_url)
            if r.status_code == 200:
                return r.text
            else:
                CrawlerLogger.logger.warning("request catalog_url error {0} status: {1}".format(self.seed_url, r.status_code))
                return ""
        except Exception as e:
            CrawlerLogger.logger.error("request catalog_url error {0} {1}".format(self.seed_url, e))
            return ""

    @staticmethod
    def get_list_url(query_html_text):
        """
        找到query_html_text内所有符合要求的 url 并去掉无关字符
        :param query_html_text: 被搜索的文本
        :return: list_url :符合要求的的 url 的 list
        """
        list_url = list()
        html = etree.HTML(query_html_text)
        #tmp_list_url = html.xpath('//div[@class="rich_media_content "]/p/a/@href')  # 结果是 list类型
        tmp_list_url = html.xpath('//div[@class="rich_media_content "]/h2/a/@href')  # 结果是 list类型

        for tmp_url in tmp_list_url:  # 去掉无关字符
            url = tmp_url.replace('&scene=21', '').replace('#wechat_redirect', '').replace('#amp;', '')
            list_url.append(url)
        CrawlerLogger.logger.info(str(len(list_url)) + " urls have been found.")
        print type(html)
        return list_url

    def get_doc_from_content(self, content, detail_url):
        html = etree.HTML(content)
        title = util.get_text(html, '//title', True)  # False 时返回的是一个对象
        snippet = ''
        # cover = re.findall(r"var msgList = (.*)]};", html_text)
        cover_list = re.findall(r'data-src="(http.+?)"', content, re.I)
        cover = cover_list[len(cover_list)/2]
        tmp_meta = html.xpath('//em[@class="rich_media_meta rich_media_meta_text"]')
        detail_url = detail_url + '#rd'
        print detail_url
        if len(tmp_meta) > 1:
            author = tmp_meta[1].text
        else:
            author = util.get_text(html, '//em[@id="post-user"]', True)
        publish_time = tmp_meta[0].text
        time_struct = time.strptime(publish_time, "%Y-%m-%d")
        published_time = int(time.mktime(time_struct))
        # channel = tmp_meta[2]

        doc = Doc(self.source, title, detail_url, snippet, cover, author, self.channel, published_time)
        CrawlerLogger.logger.info("get doc" + str(doc))
        return doc


if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    # adapter = MediaPressAdapter(
    #     seed_url='http://weixin.sogou.com/weixin?type=1&query=non-exist-FAA')
    seed_url_2015 = 'http://mp.weixin.qq.com/s?__biz=MzIxNzA0NzM4NA==&mid=503776257&idx=5&sn=b977558f41d234c362ac9fae5435909f&chksm=0c0c6c363b7be5208907f2e3cf4625b7d79f8bb80533b45f3734a2bca11ba1fc214bc977207f&scene=20#rd'
    seed_url_2016_1= 'http://mp.weixin.qq.com/s?__biz=MzIxNzA0NzM4NA==&mid=503776257&idx=4&sn=9b133719cf968378536115b1e648d549&chksm=0c0c6c363b7be5206f7c548e5c6fcac975576ca836ee63dd3af0d04f7415e4ca9f514612446a'

    seed_url_2016_3='http://mp.weixin.qq.com/s?__biz=MzIxNzA0NzM4NA==&mid=503776257&idx=2&sn=2ffedd7111678862252c923fad1a286a&chksm=0c0c6c363b7be5207147958dda1ef637a9fdf846805122d30b81e11f2cf51c875590c02d4ff7&mpshare=1&scene=1&srcid=1219rpyFanSzjtmbsvxeJTTZ#rd'
    seed_url_2016_4='http://mp.weixin.qq.com/s?__biz=MzIxNzA0NzM4NA==&mid=503776257&idx=1&sn=1a99f839fecc5e6d69073accf2f2d8a2&chksm=0c0c6c363b7be520f4926c8552c5eccdcc271a8d4f14b6e023e3b562fe6188950fdbbef6a68c&mpshare=1&scene=1&srcid=1219Hte8Fc9V9p2V1FzZbTG2#rd'
    adapter = NonExistAdapter(
        seed_url=seed_url_2016_4, channel=u"不存在")
    adapter.get_docs()
    # ls = "http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==\x26amp;mid=2650721480\x26amp;idx=1\x26amp;sn=191cb46a8ebbb71519d5d668705aa81b\x26amp;chksm=871b08b6b06c81a0265fc5de459f78cd5e1e887f3569f57a2e7ccb4ff7835d73c66699cc483a#rd"
    # print ls.replace('\x26amp;', '&')


